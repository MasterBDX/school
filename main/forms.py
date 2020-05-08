from django import forms

from school_tabels.models import TheClass
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

from .models import SchoolInfo, MainArticle


class Contact(forms.Form):
    name = forms.CharField(label='الإسم', widget=forms.TextInput())
    email = forms.EmailField(label='الإيميل', widget=forms.TextInput())
    phone_number = forms.CharField(
        label='رقم الهاتف', widget=forms.TextInput())
    subject = forms.CharField(label='الموضوع', widget=forms.TextInput())
    message = forms.CharField(label='المحتوى', widget=forms.Textarea())


class ResultSearchForm(forms.Form):
    the_class = forms.ModelChoiceField(
        queryset=TheClass.objects.all(), label='الصف')
    id_num = forms.CharField(label='رقم القيد / الرقم الوطني')


class SchoolInfoForm(forms.ModelForm):
    class Meta:
        model = SchoolInfo
        fields = '__all__'
        widgets = {
            'content': SummernoteWidget(attrs={'summernote': {'toolbar': [
                ['style', ['style']],
                ['font', ['bold', 'underline', 'clear']],
                ['fontname', ['fontname']],
                ['color', ['color']],
                ['para', ['ul', 'ol', 'paragraph']],
                ['table', ['table']],
                ['insert', ['link', 'picture', 'video']],
                ['view', ['fullscreen', 'codeview', 'help']],
            ]}}),
            # 'content': SummernoteInplaceWidget(),
        }


class MainArticleForm(forms.ModelForm):
    class Meta:
        model = MainArticle
        fields = '__all__'
