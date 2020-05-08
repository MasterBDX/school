import datetime
from django import forms

from .models import (
    Exam, ExamTabel,
    TheClass, SchoolSchedule, Day,
    Article, ClassRoom
)

from .vars import *


class AddSubjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = 'إسم المادة'

    class Meta:
        model = Article
        fields = '__all__'


class AddClassForm(forms.ModelForm):
    name = forms.CharField(label='إسم الصف', widget=forms.TextInput(
        attrs={'placeholder': 'أدخل إسم الفصل : الثامن على سبيل المثال'}))
    order = forms.IntegerField(label='ترتيب الظهور')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["subjects"].help_text = 'يرجى الضغط على زر ctrl و إختيار المواد الدراسية لهذا الفصل '
        self.fields["subjects"].label = 'المواد الدراسية'

    class Meta:
        model = TheClass
        exclude = ['subjects_num']


class AddClassRoomForm(forms.ModelForm):
    class Meta:
        model = ClassRoom
        fields = '__all__'
        labels = {'name': 'إسم الفصل',
                  'order': 'ترتيب الظهور',
                  'the_class': 'الصف'}


class AddExamTabelForm(forms.ModelForm):
    class Meta:
        model = ExamTabel
        exclude = ['last_update_by']
        labels = {
            'year': 'السنة',
            'the_class': 'الصف',
            'exam_type': 'نوع الإمتحان',
            'semester': 'الفترة',
            'class_room': 'الفصل الدراسي'
        }


class AddExamForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['article'].required = False
        self.fields['the_date'].required = False
        self.fields['the_date'].widget = forms.SelectDateWidget(
            empty_label=('السنة', 'الشهر', 'اليوم'),
            years=YEARS_,
            months=MONTHS)

    class Meta:
        model = Exam
        exclude = ['exam_tabel', 'day']
        labels = {
            'article': 'المادة',
            'the_date': 'تاريخ الإمتحان',
            'start_time': 'وقت بداية الإمتحان',
            'end_time': 'وقت نهاية الإمتحان',
        }


class AddFullScheduleForm(forms.Form):
    class_room = forms.ModelChoiceField(
        label='الفصل الدراسي', queryset=ClassRoom.objects.all())

    def clean(self):
        class_room = self.cleaned_data.get('class_room')
        days = class_room.days.all()
        if days.count() > 5:
            raise forms.ValidationError('لقد أدخلت جميع الحصص لهذا الفصل')


class AddFullScheduleModelForm(forms.ModelForm):
    day = forms.ModelChoiceField(
        label='اليوم', queryset=Day.objects.all())

    class_1 = forms.ModelChoiceField(
        label='الحصة الاولى', queryset=Article.objects.all())
    class_2 = forms.ModelChoiceField(
        label='الحصة الثانية', queryset=Article.objects.all())
    class_3 = forms.ModelChoiceField(
        label='الحصة الثاثة', queryset=Article.objects.all())
    class_4 = forms.ModelChoiceField(
        label='الحصة الرابعة', queryset=Article.objects.all())
    class_5 = forms.ModelChoiceField(
        label='الحصة الخامسة', queryset=Article.objects.all())
    class_6 = forms.ModelChoiceField(
        label='الحصة السادسة', queryset=Article.objects.all())
    class_7 = forms.ModelChoiceField(
        label='الحصة السابعة', queryset=Article.objects.all())

    class Meta:
        model = SchoolSchedule
        exclude = ['class_room']


class ChooseExamInfoForm(forms.Form):
    the_class = forms.ModelChoiceField(
        label='الصف', queryset=TheClass.objects.all())
    semester = forms.ChoiceField(
        label='الفترة', choices=SEMESTERS)


class ScheduleSearchForm(forms.Form):
    class_room = forms.ModelChoiceField(label='الفصل الدراسي',
                                        help_text='يرجى إختيار الفصل ثم الضعط على بحث',
                                        queryset=ClassRoom.objects.all())


current_year = datetime.date.today().year


class ExamsTabelSearchForm(forms.Form):
    year = forms.ChoiceField(
        label='السنة', choices=YEARS, initial=current_year)
    the_class = forms.ModelChoiceField(label='الصف الدراسي',
                                       queryset=TheClass.objects.all())
    exam_type = forms.ChoiceField(choices=TYPE, label='نوع الإمتحان')
    semester = forms.ChoiceField(choices=SEMESTERS, label='الفترة')
    class_room = forms.ModelChoiceField(label='الفصل الدراسي',
                                        queryset=ClassRoom.objects.all())
