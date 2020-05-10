from django import forms

from school_tabels.models import TheClass
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django.utils.translation import ugettext_lazy as _
from .models import SchoolInfo, MainArticle

import re


class Contact(forms.Form):
    name = forms.CharField(label=_('Name'), widget=forms.TextInput())
    email = forms.EmailField(label=_('Email'),
                             error_messages={
                                 'invalid': _('Please enter a valid email')},
                             widget=forms.TextInput())
    phone_number = forms.CharField(
        label=_('Phone Number'), widget=forms.TextInput())
    subject = forms.CharField(label=_('Subject'), widget=forms.TextInput())
    message = forms.CharField(label=_('Content'), widget=forms.Textarea())

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        matches = re.findall(r'^09\d{8}$', phone_number)
        if not matches:
            raise forms.ValidationError(
                _('Please enter a valid phone number '))
        return phone_number


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
