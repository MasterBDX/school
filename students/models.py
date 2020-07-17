from django.db import models
from django_countries.fields import CountryField
from django.urls import reverse
from django_resized import ResizedImageField

from school_tables.models import TheClass, Article, ClassRoom
from .managers import SemesterManager, StudentManager

from .mixins.common_functions_mixin import SubjectsResultsMixin, FinalResultsMixin
from .mixins.compensatory_exams_functions_mixin import CompensatoryExamsFunctionsMixin
from .mixins.result_paper_functions_mixin import ResultPaperFunctionMixin
from .mixins.semester_fucntions_mixin import SemesterFunctionMixin
from .mixins.subject_result_function_mixin import SubjectResultFunctionMixin

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


class ResultsPaper(models.Model,ResultPaperFunctionMixin, FinalResultsMixin):
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
    
    total = models.CharField(max_length=255,
                             blank=True,null=True)
    percentage = models.FloatField(blank=True,null=True)
    
    estimate = models.CharField(max_length=255,
                             blank=True,null=True)
    

    class Meta:
        ordering = ['the_class']

    def __str__(self):
        return '{} {} {} {}'.format('صحيفة', self.student.get_std_name(),
                                    'للصف', self.the_class.name)

    def get_absolute_url(self):
        return reverse('students:detail', kwargs={'pk': self.student.pk})


class Semester(models.Model,SemesterFunctionMixin, FinalResultsMixin):
    results_paper = models.ForeignKey(ResultsPaper,
                                      on_delete=models.CASCADE,
                                      related_name='semesters')
    order = models.CharField(max_length=255,
                             choices=ORDER, default="1")
    active = models.BooleanField(default=False)
    total = models.CharField(max_length=255,
                             blank=True,null=True)
    percentage = models.FloatField(blank=True,null=True)
    
    estimate = models.CharField(max_length=255,
                             blank=True,null=True)

    class Meta:
        ordering = ['order']

    objects = SemesterManager()

    def __str__(self):
        return self.results_paper.student.get_std_name() + \
            ' سمستر ' + str(self.order) + ' ' + self.results_paper.__str__()

    def get_absolute_url(self):
        return self.results_paper.get_absolute_url()




class SubjectResult(models.Model,SubjectResultFunctionMixin, SubjectsResultsMixin):
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


class CompensatoryExam(models.Model,CompensatoryExamsFunctionsMixin, SubjectsResultsMixin):
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
    total = models.CharField(max_length=255,
                             blank=True,null=True)
    results_paper = models.ForeignKey(
        ResultsPaper, on_delete=models.CASCADE,
         related_name='all_com_grades')

    class Meta:
        ordering = ['subject',]

    def __str__(self):
        return '{} مادة - {} الدور - {} الفترة'.format(self.subject.name,
                                                       self.part,
                                                       self.semester)

    
