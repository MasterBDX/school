from django.db import models
from django_countries.fields import CountryField
from django.urls import reverse
from django_resized import ResizedImageField

from school_tabels.models import TheClass, Article, ClassRoom
from .managers import SemesterManager, StudentManager
from .mixins import SubjectsResultsMixin, FinalResultsMixin

from main.utils import students_image_random_name
from main.vars import *


class Student(models.Model):
    first_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    grand_father_name = models.CharField(max_length=255)
    mother_name = models.CharField(max_length=255)

    full_name = models.CharField(max_length=255)
    place_of_birth = models.CharField(max_length=255)
    birth_date = models.DateField()
    gender = models.CharField(max_length=255, choices=GENDER)
    cell_phone = models.CharField(max_length=255, null=True, blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    the_class = models.ForeignKey(
        TheClass, related_name='students', on_delete=models.CASCADE)
    classroom = models.ForeignKey(
        ClassRoom, related_name='students', on_delete=models.CASCADE)
    nid_number = models.CharField(max_length=255, null=True, blank=True)
    nationality = models.CharField(
        max_length=255, default='ليبي', choices=NATIONALITY)
    image = ResizedImageField(size=[300, 300], blank=True, null=True,
                                   upload_to=students_image_random_name)
    objects = StudentManager()

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse('students:detail', kwargs={'pk': self.pk})

    def get_std_name(self):
        return "{} {} {}".format(self.first_name, self.father_name, self.surname)

    def get_full_name(self):
        return "{}  {}  {}  {}".format(self.first_name, self.father_name, self.grand_father_name, self.surname)


class ResultsPaper(models.Model, FinalResultsMixin):
    class_leader_name = models.CharField(max_length=255)
    student = models.ForeignKey(Student,
                                on_delete=models.CASCADE,
                                related_name='papers')
    entry = models.CharField(default='نظامي', max_length=255, choices=ENTRY)
    status = models.CharField(default='مستجد', max_length=255, choices=STATUS)
    the_class = models.ForeignKey(TheClass,
                                  on_delete=models.CASCADE,
                                  related_name='results')

    active = models.BooleanField(default=False)
    part2 = models.BooleanField(default=False)
    part3 = models.BooleanField(default=False)
    total = models.CharField(max_length=255,
                             blank=True,null=True)

    class Meta:
        ordering = ['the_class']

    def __str__(self):
        return '{} {} {} {}'.format('صحيفة', self.student.get_std_name(),
                                    'للصف', self.the_class.name)

    def get_absolute_url(self):
        return reverse('students:detail', kwargs={'pk': self.student.pk})

    def get_part2_grades(self):
        return self.all_com_grades.filter(part='2')

    def get_part3_grades(self):
        return self.all_com_grades.filter(part='3')

    def passed_all(self):
        lis = [x.passed_all() for x in self.semesters.active().filter(
            order=self.current_final_semester())]
        return all(lis)

    def current_final_semester(self):
        qs = self.semesters.active().values_list('order')
        semesters = [x[0] for x in qs]
        if '2' in semesters and '3' not in semesters:
            return '2'
        elif '3' in semesters:
            return '3'
        return '1'

    def current_part(self):

        if self.part2 and not self.part3:
            return '2'
        elif self.part3:
            return '3'
        return None

    def total_grades(self):
        '''this func to get total grades '''

        total, std_total = 0, 0
        qs = self.semesters.active()
        for semester in qs:
            t, s = semester.get_total_grades()
            total += t
            std_total += s
        return total, std_total

    def total_none_passed_exams(self):
        ''' this func to get the semester subjects results
             exams grades that not passed yet '''

        order = self.current_final_semester()
        total = 0
        if int(order) > 1:
            qs = self.semesters.filter(order=order)
            total = sum([x.none_passed_exams_grade() for x in qs])
        return total

    def total_comps_grades(self, part=''):
        '''this func to get total grades for just the part 1 results '''
        qs = self.all_com_grades.filter(
            part=part).values_list('std_exam_grade')
        return self.get_total_by_qs(qs)

    def get_total_grades(self):
        ''' this func to manage how to get total grades
             whether if part2 or part3 are active '''

        total, std_total = self.total_grades()
        if self.part2 and not self.part3:
            std_total = std_total - self.total_none_passed_exams() + \
                self.total_comps_grades(
                part='2')
        elif self.part3:
            std_total = std_total - self.total_none_passed_exams() + \
                self.total_comps_grades(
                part='3')
        return total, std_total


class Semester(models.Model, FinalResultsMixin):
    results_paper = models.ForeignKey(ResultsPaper,
                                      on_delete=models.CASCADE,
                                      related_name='semesters')
    order = models.CharField(max_length=255,
                             choices=ORDER, default="1")
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    objects = SemesterManager()

    def __str__(self):
        return self.results_paper.student.get_std_name() + \
            ' سمستر ' + str(self.order) + ' ' + self.results_paper.__str__()

    def get_absolute_url(self):
        return self.results_paper.get_absolute_url()

    def passed_all(self):
        passed = 0
        qs = self.subjects_results.values_list('passed', 'subject')
        for x in qs:
            if x[0] == True:
                passed += 1
            else:
                part = self.results_paper.current_part()
                if part:
                    comp = self.results_paper.all_com_grades.filter(semester=self.order,
                                                                    subject=x[1],
                                                                    results_paper=self.results_paper,
                                                                    part=part)
                    if comp.count() == 1:
                        comp = comp.first()
                        if comp.passed:
                            passed += 1
        return passed == qs.count()

    def get_total_grades(self):
        qs = self.subjects_results.values_list('exam_grade',
                                               'year_works_grade')
        qs2 = self.subjects_results.values_list('std_exam_grade',
                                                'std_year_works_grade')
        total = sum([sum(x) for x in qs])
        std_total = sum([sum(x) for x in qs2])
        return total, std_total

    def none_passed_exams_grade(self):
        qs = self.subjects_results.filter(
            passed=False).values_list('std_exam_grade')
        return self.get_total_by_qs(qs)


class SubjectResult(models.Model, SubjectsResultsMixin):
    subject = models.ForeignKey(
        Article, on_delete=models.CASCADE,
        related_name="results",
        blank=True,
        null=True)
    exam_grade = models.PositiveIntegerField(default=0)
    exam_pass_grade = models.PositiveIntegerField(default=0)
    year_works_grade = models.PositiveIntegerField(default=0)

    grade_pass_subject = models.PositiveIntegerField(default=0)
    std_exam_grade = models.PositiveIntegerField(default=0)
    std_year_works_grade = models.PositiveIntegerField(default=0)
    passed = models.BooleanField(default=False)
    semester = models.ForeignKey(
        Semester, related_name='subjects_results',
        on_delete=models.CASCADE,
        blank=True,
        null=True)

    class Meta:
        ordering = ['subject']

    def __str__(self):
        return self.semester.order + ' ' + self.subject.name \
            + ' الصف ' + self.semester.results_paper.the_class.name \
            + ' الطالب ' + self.semester.results_paper.student.get_std_name()

    def total_subject_grades(self):
        std_grades, grades = self.get_total()
        if self.semester.order == '3':
            std_grades, grades = self.get_semester3_total()
        return '{} / {} '.format(std_grades, grades)

    def total_subject_year_grades(self):
        std_total, total = self.std_year_works_grade, self.year_works_grade
        qs = SubjectResult.objects.filter(
            subject=self.subject,
            semester__results_paper=self.semester.results_paper).exclude(id=self.id)
        if qs.exists():
            for obj in qs:
                s, t = obj.get_total()
                std_total += s
                total += t
        return std_total, total

    def get_total_subject_grades(self):
        s, t = self.total_subject_year_grades()
        return '{} / {}'.format(s, t)

    def get_semester3_total(self):
        s, t = self.total_subject_year_grades()
        total = self.exam_grade + t
        std_total = self.std_exam_grade + s
        return std_total, total


class ClassGrade(models.Model):
    subject = models.ForeignKey(
        Article, on_delete=models.CASCADE,
        related_name="classes_grades",
        blank=True,
        null=True)
    exam_grade = models.PositiveIntegerField(default=0)
    exam_pass_grade = models.PositiveIntegerField(default=0)
    grade_pass_subject = models.PositiveIntegerField(default=0)
    year_works_grade = models.PositiveIntegerField(default=0)

    the_class = models.ForeignKey(
        TheClass, related_name='grades', on_delete=models.CASCADE)
    order = models.CharField(max_length=255,
                             choices=ORDER, default="1")

    class Meta:
        ordering = ['subject']

    def __str__(self):
        return self.subject.name + ' ' + self.order + ' ' + self.the_class.name


class CompensatoryExam(models.Model, SubjectsResultsMixin):
    subject = models.ForeignKey(
        Article, on_delete=models.CASCADE,
        related_name="com_grades",
        blank=True,
        null=True)
    exam_grade = models.PositiveIntegerField(default=0)
    exam_pass_grade = models.PositiveIntegerField(default=0)
    year_works_grade = models.PositiveIntegerField(default=0)
    grade_pass_subject = models.PositiveIntegerField(default=0)
    std_year_works_grade = models.PositiveIntegerField(default=0)
    std_exam_grade = models.PositiveIntegerField(default=0)
    passed = models.BooleanField(default=False)
    semester = models.CharField(choices=SEMESTER, default='2', max_length=120)
    part = models.CharField(choices=PART, max_length=120)

    results_paper = models.ForeignKey(
        ResultsPaper, on_delete=models.CASCADE, related_name='all_com_grades')

    class Meta:
        ordering = ['subject',]

    def __str__(self):
        return '{} مادة - {} الدور - {} الفترة'.format(self.subject.name,
                                                       self.part,
                                                       self.semester)

    def total_subject_grades(self):
        std_grades, grades = self.get_total()
        return '{} / {} '.format(std_grades, grades)
