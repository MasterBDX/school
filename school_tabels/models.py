from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language

from main.vars import *


class Day(models.Model):
    name = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def get_name(self):
        _('Saturday')
        _('Sunday')
        _('Monday')
        _('Tuesday')
        _('Wednsday')
        _('Thursday')
        _('Friday')
        return str(_(self.name))

    def __str__(self):
        return self.get_name()


class Article(models.Model):
    name = models.CharField(max_length=255)
    en_name = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_name(self):
        lang = get_language()
        name = self.name
        if lang == 'en':
            name = self.en_name
        return name

    def __str__(self):
        name = self.get_name()
        return name


class TheClass(models.Model):
    name = models.CharField(max_length=255)

    timestamp = models.DateTimeField(auto_now_add=True)
    subjects = models.ManyToManyField(
        Article, blank=True)
    subjects_num = models.PositiveSmallIntegerField(default=7)
    updated = models.DateTimeField(auto_now=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Classes'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_mid_exams(self):
        return self.exams_tabel.filter(exam_type=1)

    def get_final_exams(self):
        return self.exams_tabel.exclude(exam_type=1)


class ClassRoom(models.Model):
    name = models.CharField(max_length=255)
    the_class = models.ForeignKey(TheClass, on_delete=models.CASCADE,
                                  related_name='classrooms')
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'classrooms'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_results(self):
        results = self.the_class.results.filter(
            student__classroom=self).values_list('student__id')
        return [x[0] for x in results]

    def get_stds_count(self):
        return self.students.same_class(self.the_class.id).count()


class ExamTabel(models.Model):
    title = models.CharField(max_length=255)
    en_title = models.CharField(max_length=255, blank=True, null=True)
    year = models.CharField(choices=YEARS, max_length=50)
    the_class = models.ForeignKey(
        TheClass, related_name='exams_tabel', on_delete=models.CASCADE)
    exam_type = models.CharField(max_length=255,
                                 choices=TYPE,
                                 default=1)
    last_editor = models.CharField(max_length=255, null=True,
                                   blank=True)
    semester = models.CharField(max_length=255,
                                choices=SEMESTERS,
                                default=1)
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE,
                                   related_name='exam_tabels',
                                   null=True,
                                   blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['semester', 'exam_type', 'class_room']

    def __str__(self):
        return self.semester + ' الفترة ' + self.the_class.name + ' ' + ' جدول إمتحانات الصف '


class Exam(models.Model):
    exam_tabel = models.ForeignKey(ExamTabel, on_delete=models.CASCADE,
                                   related_name='exams',
                                   null=True, blank=True)
    subject = models.CharField(max_length=255,)

    day = models.ForeignKey(
        Day, on_delete=models.CASCADE,
        null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    the_date = models.DateField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['the_date', 'start_time']

    def __str__(self):
        return self.subject + ' ' + ' إمتحان ' + self.exam_tabel.__str__()


class SchoolSchedule(models.Model):
    day = models.ForeignKey(Day,
                            on_delete=models.CASCADE)
    class_room = models.ForeignKey(ClassRoom,
                                   related_name='days',
                                   on_delete=models.CASCADE)
    class_1 = models.ForeignKey(
        Article, related_name='class_1',  on_delete=models.CASCADE)
    class_2 = models.ForeignKey(
        Article, related_name='class_2',  on_delete=models.CASCADE)
    class_3 = models.ForeignKey(
        Article, related_name='class_3',  on_delete=models.CASCADE)
    class_4 = models.ForeignKey(
        Article, related_name='class_4',  on_delete=models.CASCADE)
    class_5 = models.ForeignKey(
        Article, related_name='class_5',  on_delete=models.CASCADE)
    class_6 = models.ForeignKey(
        Article, related_name='class_6',  on_delete=models.CASCADE)
    class_7 = models.ForeignKey(
        Article, related_name='class_7',  on_delete=models.CASCADE)

    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return ' حصص ' + self.day.name

    class Meta:
        ordering = ['day']
