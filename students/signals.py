import datetime

from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save


from .models import (Student, ResultsPaper, Semester,
                     SubjectResult, ClassGrade, CompensatoryExam)


@receiver(pre_save, sender=Student)
def get_student_info(sender, instance, *args, **kwargs):
    ''' get the rest of student info '''
    if not instance.full_name:
        full_name = "{} {} {} {}".format(
            instance.first_name, instance.father_name, instance.grand_father_name, instance.surname)
        instance.full_name = full_name
    if not instance.age:
        age = datetime.date.today() - instance.birth_date

        try:
            instance.age = int(age.days / 365)
        except:
            pass


def get_subjects_results(semesters, instance):
    subjects = instance.the_class.subjects.all()
    for semester in semesters:
        qs = SubjectResult.objects.filter(
            semester=semester).exclude(semester__results_paper__the_class=instance.the_class)
        if qs.exists():
            qs.delete()
        for subject in subjects:
            qs2 = ClassGrade.objects.filter(subject=subject,
                                            the_class=instance.the_class,
                                            order=semester.order)
            if qs2.exists() and qs2.count() == 1:
                subject_result = qs2.first()
                queryset, created = SubjectResult.objects.get_or_create(
                    exam_grade=subject_result.exam_grade,
                    exam_pass_grade=subject_result.exam_pass_grade,
                    grade_pass_subject=subject_result.grade_pass_subject,
                    year_works_grade=subject_result.year_works_grade,
                    subject=subject, semester=semester)

    return True


@receiver(pre_save, sender=ResultsPaper)
def complete_the_results_paper_presave(sender, instance, *args, **kwargs):
    semesters = Semester.objects.filter(results_paper=instance)
    if semesters.exists():
        get_subjects_results(semesters, instance)


@receiver(post_save, sender=ResultsPaper)
def complete_the_results_paper_postsave(sender, instance, created, *args, **kwargs):
    if created:
        semester1, created = Semester.objects.get_or_create(
            results_paper=instance, order=1)
        semester2, created = Semester.objects.get_or_create(
            results_paper=instance, order=2)
        semester3, created = Semester.objects.get_or_create(
            results_paper=instance, order=3)
        semesters = [semester1, semester2, semester3]
        get_subjects_results(semesters, instance)


@receiver(post_save, sender=ClassGrade)
def fix_changed_results(sender, instance, created, *args, **kwargs):
    subjects = SubjectResult.objects.filter(
        semester__results_paper__the_class=instance.the_class,
        subject=instance.subject,
        semester__order=instance.order)

    if subjects.exists():
        for subject in subjects:
            subject.exam_grade = instance.exam_grade
            subject.exam_pass_grade = instance.exam_pass_grade
            subject.year_works_grade = instance.year_works_grade
            subject.grade_pass_subject = instance.grade_pass_subject
            subject.save()


def can_pass(instance, subject_result=None, semester=None):
    std_total, total = instance.get_total()
    if not subject_result:
        subject_result = instance
        if semester == '3':
            std_total, total = subject_result.get_semester3_total()
    if instance.std_exam_grade >= subject_result.exam_pass_grade:
        if std_total >= instance.grade_pass_subject:
            instance.passed = True
        else:
            instance.passed = False
    else:
        instance.passed = False


@receiver(pre_save, sender=SubjectResult)
def get_pass_boolean(sender, instance, *args, **kwargs):
    std_total, total = instance.get_total()
    qs = CompensatoryExam.objects.filter(subject=instance.subject,
                                         semester=instance.semester.order,
                                         results_paper=instance.semester.results_paper)
    if qs.count() == 1:
        com_exam = qs.first()
        com_exam.save()

    can_pass(instance, semester=instance.semester.order)


@receiver(pre_save, sender=CompensatoryExam)
def get_compen_info(sender, instance, *args, **kwargs):
    qs = SubjectResult.objects.filter(
        semester__results_paper=instance.results_paper,
        subject=instance.subject,
        semester__order=instance.semester)
    if qs.exists() and qs.count() == 1:
        subject_result = qs.first()
        instance.exam_grade = subject_result.exam_grade
        instance.exam_pass_grade = subject_result.exam_pass_grade
        if instance.semester != '3':
            instance.year_works_grade = subject_result.year_works_grade
            instance.std_year_works_grade = subject_result.std_year_works_grade
        else:
            std_total, total = subject_result.total_subject_year_grades()
            instance.year_works_grade = total
            instance.std_year_works_grade = std_total

        instance.grade_pass_subject = subject_result.grade_pass_subject
        std_total, total = instance.get_total()
        can_pass(instance, subject_result=subject_result)
