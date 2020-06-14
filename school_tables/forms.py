import datetime
import re

from django import forms
from django.utils.translation import pgettext_lazy, ugettext_lazy as _

from .models import (
    Exam, ExamTable,
    TheClass, SchoolSchedule, Day,
    Article, ClassRoom
)

from main.vars import (YEARS, YEARS_, BIRTH_YEARS, MONTHS,
                       SEMESTERS, TYPE)


class AddSubjectForm(forms.ModelForm):
    class Meta:
        help_texts = {
            'name': _('Please don\'t forget to add al altaerif to the subject name')}
        labels = {'name': _('Subject Arabian Name'),
                  'en_name': _('Subject English Name')}
        model = Article
        fields = '__all__'

    def clean_en_name(self):
        en_name = self.cleaned_data.get('en_name')
        if not re.findall('^[a-zA-Z\s]+$', en_name):
            raise forms.ValidationError(
                _("This field must have just english letters"))
        return en_name


class AddClassForm(forms.ModelForm):
    class Meta:
        labels = {'name': _('Class Name'),
                  'order': _('Appearance Order'),
                  'subjects': _('Subjects')
                  }
        help_texts = {'name': _('Please write the class name in this format (الثامن, التاسع)'),
                      'subjects': _('Please click the ctrl button and choose the subjects  for this Class')}
        model = TheClass
        exclude = ['subjects_num']


class AddClassRoomForm(forms.ModelForm):
    class Meta:
        model = ClassRoom
        fields = '__all__'
        labels = {'name': 'إسم الفصل',
                  'order': 'ترتيب الظهور',
                  'the_class': 'الصف'}


class AddExamTableForm(forms.ModelForm):
    class Meta:
        model = ExamTable
        exclude = ['last_editor']
        labels = {
            'title': _('Title'),
            'en_title': _('English Title'),
            'year': _('Year'),
            'the_class': _('Class'),
            'exam_type': _('Exams Type'),
            'semester': _('Semester'),
            'class_room': _('Classroom')
        }


class AddExamForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].required = False
        self.fields['the_date'].required = False
        self.fields['the_date'].widget = forms.SelectDateWidget(
            empty_label=(_('Year'), _('Month'), _('Day')),
            years=YEARS_,
            months=MONTHS)
        self.fields['start_time'].widget = forms.TimeInput(format='%H:%M')
        self.fields['end_time'].widget = forms.TimeInput(format='%H:%M')

    class Meta:
        model = Exam
        exclude = ['exam_table', 'day']
        labels = {
            'subject': pgettext_lazy('for Subjects', 'Subject'),
            'the_date': _('Exam Date'),
            'start_time': _('Exam start time'),
            'end_time': _('Exam end time'),
        }


class AddFullScheduleForm(forms.Form):
    class_room = forms.ModelChoiceField(
        label=_('Class'), queryset=ClassRoom.objects.all())


class AddFullScheduleModelForm(forms.ModelForm):
    class Meta:
        labels = {
            'day': _('Day'),
            'class_1': _('First Class'),
            'class_2': _('Second Class'),
            'class_3': _('Third Class'),
            'class_4': _('Fourth Class'),
            'class_5': _('Fifth Class'),
            'class_6': _('Sixth Class'),
            'class_7': _('Seventh Class')
        }
        model = SchoolSchedule
        exclude = ['class_room']


class ChooseExamInfoForm(forms.Form):
    the_class = forms.ModelChoiceField(
        label='الصف', queryset=TheClass.objects.all())
    semester = forms.ChoiceField(
        label='الفترة', choices=SEMESTERS)


class ScheduleSearchForm(forms.Form):
    class_room = forms.ModelChoiceField(label=_('Classroom'),
                                        queryset=ClassRoom.objects.all())


current_year = datetime.date.today().year


class ExamstableSearchForm(forms.Form):
    year = forms.ChoiceField(
        label=_('Year'), choices=YEARS, initial=current_year)
    the_class = forms.ModelChoiceField(label=_('Class'),
                                       queryset=TheClass.objects.all())
    exam_type = forms.ChoiceField(choices=TYPE, label=_('Exam Type'))
    semester = forms.ChoiceField(choices=SEMESTERS, label=_('Semester'))
    class_room = forms.ModelChoiceField(label=_('Classroom'),
                                        queryset=ClassRoom.objects.all(),
                                        help_text=_('if the exams Table for all classrooms please let this field empty'))
