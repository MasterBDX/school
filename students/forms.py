from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from django.utils import timezone

from school_tabels.models import TheClass, Article
from main.vars import *
from students.models import (Student, ResultsPaper,
                             SubjectResult, CompensatoryExam)


class AddStudent(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birth_date'].widget = forms.SelectDateWidget(
            empty_label=('السنة', 'الشهر', 'اليوم'), years=BIRTH_YEARS, months=MONTHS)

        # self.fields['birth_date'].error_messages = {
        #     'invalid': 'يرجى إدخال التاريخ بطريقة صحيحة'}

        self.fields['nationality'].initial = 'ليبي'

    class Meta:
        labels = {'first_name': 'الإسم الأول', 'father_name': 'إسم الأب',
                  'grand_father_name': 'إسم الجد', 'surname': 'اللقب',
                  'mother_name': 'إسم الأم', 'place_of_birth': 'مكان الولادة',
                  'birth_date': 'تاريخ الميلاد', 'gender': 'الجنس',
                  'cell_phone': 'رقم الهاتف', 'id_number': 'الرقم الوطني',
                  'the_class': 'الصف', 'nationality': 'الجنسية',
                  'classroom': 'الفصل الدراسي'
                  }
        error_messages = {
            'birth_date': {
                'invalid': 'يرجى إدخال التاريخ بطريقة صحيحة'}
        }
        model = Student
        exclude = ['age', 'full_name']


class SelectSubjectForm(forms.Form):
    subject = forms.ModelChoiceField(
        label='المادة', queryset=Article.objects.all())


class AddResultsPaperForm(forms.ModelForm):

    class Meta:
        labels = {'class_leader_name': 'رائد الفصل',
                  'entry': 'صفة القيد', 'status': 'حالة الطالب',
                  'the_class': 'الصف', 'active': 'تنشيط', 'part2': 'إظهار الدور الثاني',
                  'part3': 'إظهار الدور الثالث'}
        model = ResultsPaper
        fields = '__all__'
        exclude = ['student']


class AddSubjectResultForm(forms.ModelForm):
    class Meta:
        labels = {'std_exam_grade': 'درجة الإمتحان',
                  'std_year_works_grade': 'درجة باقي أعمال السنة'}
        model = SubjectResult
        exclude = ['semester', 'subject', 'exam_grade', 'grade_pass_subject',
                   'exam_pass_grade', 'year_works_grade', 'passed']


class AddClassGradesForm(forms.ModelForm):
    exam_grade = forms.IntegerField(initial=0, label='درجة الإمتحان')
    exam_pass_grade = forms.IntegerField(
        initial=0, label='درجة النجاح في الإمتحان')
    grade_pass_subject = forms.IntegerField(
        initial=0, label='درجة النجاح في المادة')
    year_works_grade = forms.IntegerField(
        initial=0, label='درجة باقي أعمال السنة')

    class Meta:
        model = SubjectResult
        exclude = ['subject', 'order', 'the_class']


class AddCompensatoryExamForm(forms.ModelForm):
    class Meta:
        labels = {'subject': 'المادة',
                  'std_exam_grade': 'درجة الإمتحان للطالب',
                  'semester': 'الفترة', 'part': 'الدور'}
        model = CompensatoryExam
        exclude = ['passed', 'the_class',
                   'results_paper', 'exam_grade',
                   'exam_pass_grade', 'year_works_grade',
                   'grade_pass_subject', 'std_year_works_grade',
                   ]

    def int_checker(self, num):
        try:
            num = int(num)
            return num
        except:
            return None

    def pass_checker(self, subject, semester):
        p_id = self.int_checker(self.data.get('p'))
        if p_id:
            qs = SubjectResult.objects.filter(
                semester__results_paper__id=p_id,
                subject=subject,
                semester__order=semester
            )

            if qs.exists():
                qs = qs.filter(passed=False)
                if qs.count() == 1:
                    return True, ' '
                return False, 'الطالب لم يرسب في هذه المادة'
            return False, ' لا يوجد مادة {} لهذا الصف'.format(subject.name)

        raise forms.ValidationError('لقد حدث خطأ يرجى تجديد الصفحة')

    def clean(self):
        data = self.cleaned_data
        subject = data.get('subject')
        semester = data.get('semester')
        passed, error_msg = self.pass_checker(subject, semester)
        if passed:
            return data
        raise forms.ValidationError(error_msg)


class EditCompensatoryExamForm(forms.ModelForm):
    class Meta:
        labels = {
            'std_exam_grade': 'درجة الإمتحان للطالب',
            'semester': 'الفترة',
        }
        model = CompensatoryExam
        fields = ['std_exam_grade', 'semester']
