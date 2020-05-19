import datetime
from django.db.models.signals import pre_save, m2m_changed, post_save
from django.dispatch import receiver

from .models import Exam, TheClass
from students import models



@receiver(m2m_changed, sender=TheClass.subjects.through)
def get_subjects_num(sender, instance, action, *args, **kwargs):
    instance.subjects_num = instance.subjects.count()
    instance.save()
    if action == 'post_add':
        subjects = instance.subjects.all()
        semesters = models.Semester.objects.filter(
            results_paper__the_class=instance)
        for subject in subjects:
            for semester in semesters:
                models.SubjectResult.objects.get_or_create(
                    semester=semester, subject=subject)
            models.ClassGrade.objects.get_or_create(
                subject=subject, the_class=instance, order='1')
            models.ClassGrade.objects.get_or_create(
                subject=subject, the_class=instance, order='2')
            models.ClassGrade.objects.get_or_create(
                subject=subject, the_class=instance, order='3')

    if action == 'post_remove':
        subjects = instance.subjects.all()
        qs = models.ClassGrade.objects.filter(
            the_class=instance).exclude(subject__in=subjects)
        qs2 = models.SubjectResult.objects.filter(
            semester__results_paper__the_class=instance).exclude(subject__in=subjects)

        qs.delete()
        qs2.delete()


@receiver(pre_save, sender=Exam)
def get_arabic_weekday(sender, instance, *args, **kwargs):
    if not instance.day:
        WEEK_DAYS = {'1': 'الإثنين', '2': 'الثلاثاء', '3': 'الإربعاء',
                     '4': 'الخميس', '5': 'الجمعة', '6': 'السبت', '7': 'الأحد'}
        instance.day = WEEK_DAYS.get(str(instance.the_date.isoweekday()))
