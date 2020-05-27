from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from school_tabels.models import TheClass, Article
from main.vars import *
from students.models import (Student, ResultsPaper,
                             SubjectResult, CompensatoryExam)


class AddStudent(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birth_date'].widget = forms.SelectDateWidget(
            empty_label=(_('Year'), _('Month'), _('Day')),
            years=BIRTH_YEARS, months=MONTHS)
        self.fields['nationality'].initial = 'ليبي'

    class Meta:
        labels = {
                'first_name': _('First Name'), 'father_name': _('Father Name'),
                  'grand_father_name': _('Grandfather Name'), 'surname': _('Surname'),
                  'mother_name': _('Mother Name'), 'place_of_birth': _('Place Of Birth'),
                  'birth_date': _('Birth Date'), 'gender': _('Gender'),
                  'cell_phone': _('Cell Phone Number'), 'id_number': _('Id Number'),
                  'the_class': _('Class'), 'nationality': _('Nationality'),
                  'classroom': _('Classroom')
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
    class Meta:
        labels = {'exam_grade':_('Exam Grade'),
                  'exam_pass_grade':_('Exam Pass Grade'),
                  'grade_pass_subject':_('Subject Pass Grade'),
                  'year_works_grade':_('Year Works Grade')}
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
