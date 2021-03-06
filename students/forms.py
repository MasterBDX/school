from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _,get_language
from school_tables.models import TheClass, Article
from main.vars import *
from students.models import (Student, ResultsPaper,
                             SubjectResult, CompensatoryExam)
import re

class AddStudent(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birth_date'].widget = forms.SelectDateWidget(
            empty_label=(_('Year'), _('Month'), _('Day')),
            years=BIRTH_YEARS, months=MONTHS)
        self.fields['nationality'].initial = _('Libyan')

    class Meta:
        help_texts = {'nid_number':_('if student was foreign please let it empty ')}
        labels = {
                  'first_name': _('First Name'), 'father_name': _('Father Name'),
                  'grand_father_name': _('Grandfather Name'), 'surname': _('Surname'),
                  'mother_name': _('Mother Name'), 'place_of_birth': _('Place Of Birth'),
                  'birth_date': _('Birth Date'), 'gender': _('Gender'),
                  'cell_phone': _('Cell Phone Number'), 'nid_number': _('N.Id Number'),
                  'the_class': _('Class'), 'nationality': _('Nationality'),
                  'classroom': _('Classroom'),'image': _('Student Image'),
                  }
        
        model = Student
        exclude = ['age', 'full_name']
        
    def clean_cell_phone(self):
        cell_phone = self.cleaned_data.get('cell_phone')
        if cell_phone != ' ' and cell_phone != None :
            if not cell_phone.isdigit():   
                raise forms.ValidationError(_('Please enter a valid phone number'))
        return cell_phone
    
    def clean_nid_number(self):
        nid_number = self.cleaned_data.get('nid_number')
        std_id = self.data.get('id','1')
        if nid_number != ' ' and nid_number != None :   
            if not nid_number.isdigit():
                raise forms.ValidationError(_('Please enter a valid national ID number'))
            else:
                qs = Student.objects.filter(nid_number=nid_number)
                if qs.count() < 1:
                    pass
                else:
                    obj = qs.first()
                    if std_id.isdigit():
                        if std_id == obj.id:
                            pass
                        else:
                            raise forms.ValidationError(_('Student with this national number already exists'))                    
        return nid_number
    
    # def clean_cell_phone(self):
    #     cell_phone = self.cleaned_data.get('cell_phone')
    #     matches = re.findall(r'^09\d{8}$', cell_phone)
    #     if not matches:
    #         raise forms.ValidationError(_('Please enter a valid phone number'))
    #     return cell_phone

class SelectSubjectForm(forms.Form):
    subject = forms.ModelChoiceField(
        label='المادة', queryset=Article.objects.all())


class AddResultsPaperForm(forms.ModelForm):
    class Meta:
        labels = {'class_leader_name': _('Class Leader'),
                  'entry': _('Enrollment attribute'),
                  'status': _('Student Status'),
                  'the_class': _('Class'),
                  'active': _('Activate'),
                  }
        model = ResultsPaper
        fields = '__all__'
        exclude = ['student','part2','part3',
                   'total_summation','total',
                   'percentage','estimate']
    


class AddSubjectResultForm(forms.ModelForm):
    class Meta:
        labels = {'std_exam_grade': _('Exam Grade'),
                  'std_year_works_grade': _('Year Works Grade')}
        model = SubjectResult
        exclude = ['semester', 'subject', 'exam_grade', 'grade_pass_subject',
                   'exam_pass_grade', 'year_works_grade', 'passed','total']


class AddSubjectResultSemester3Form(forms.ModelForm):
    class Meta:
        labels = {'std_exam_grade': _('Exam Grade'),
                  }
        model = SubjectResult
        exclude = ['semester', 'subject', 'exam_grade', 'grade_pass_subject',
                   'exam_pass_grade', 'year_works_grade', 'passed',
                   'std_year_works_grade','total']


class AddClassGradesForm(forms.ModelForm):
    class Meta:
        labels = {'exam_grade':_('Exam Grade'),
                  'exam_pass_grade':_('Exam Pass Grade'),
                  'grade_pass_subject':_('Subject Pass Grade'),
                  'year_works_grade':_('Year Works Grade')}
        model = SubjectResult
        exclude = ['subject', 'order', 'the_class']


class AddClassGradesSemester3Form(forms.ModelForm):
    class Meta:
        labels = {'exam_grade':_('Exam Grade'),
                  'exam_pass_grade':_('Exam Pass Grade'),
                  'grade_pass_subject':_('Subject Pass Grade'),
                  }
        model = SubjectResult
        exclude = ['subject', 'order', 'the_class','year_works_grade']


class AddCompensatoryExamForm(forms.ModelForm):
    class Meta:
        labels = {'subject': _('Subject'),
                  'std_exam_grade': _('Student Exam grade'),
                  'semester': _('Semester'), 'part': _('Attempt')}

        model = CompensatoryExam
        exclude = ['passed', 'the_class',
                   'results_paper', 'exam_grade',
                   'exam_pass_grade', 'year_works_grade',
                   'grade_pass_subject', 'std_year_works_grade',
                   'total']

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
                return False, _('The student has not failed in this subject')
            msg = 'There is no {} for this class'.format(subject.en_name)
            if get_language() == 'ar':
                msg = 'لا يوجد مادة {} لهذا الصف'.format(subject.name)
            return False, msg 

        raise forms.ValidationError(_('An error has occurred, please refresh the page'))
    
    
    def clean(self):
        data = self.cleaned_data
        subject = data.get('subject')
        semester = data.get('semester')
        if subject and semester:
            passed, error_msg = self.pass_checker(subject, semester)
            if passed:
                return data
            raise forms.ValidationError(error_msg)


# class EditCompensatoryExamForm(forms.ModelForm):
#     class Meta:
#         labels = {
#             'std_exam_grade': 'درجة الإمتحان للطالب',
#             'semester': 'الفترة',
#         }
#         model = CompensatoryExam
#         fields = ['std_exam_grade', 'semester']
