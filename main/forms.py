from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django.utils.translation import ugettext_lazy as _

from .vars import SEMESTERS
from school_tables.models import TheClass
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
                _('Please enter a valid phone number'))
        return phone_number


class ResultSearchForm(forms.Form):
    the_class = forms.ModelChoiceField(
        queryset=TheClass.objects.all(),
        label=_('Class'),
        error_messages={'required': _('This field is required')})
    id_num = forms.CharField(label=_('Registration number / national number'),
                             error_messages={'required': _('This field is required')})
    semester = forms.ChoiceField(label=_('Semester'),
                                 choices=SEMESTERS)
    
    def clean_id_num(self):
        id_num = self.cleaned_data.get('id_num')
        if not id_num.isdigit():
            raise forms.ValidationError(
                _('This field must contain a positive integer'))
        return id_num


class SchoolInfoForm(forms.ModelForm):
    class Meta:
        labels = {'name':_('Name'),
                  'english_name':_('English Name'),
                  'content':_('Content'),
                  'school_phone':_('Cell Phone Number'),
                  'street':_('Street'),
                  'city':_('City'),
                  'municipality':_('Municipality'),
                  'province':_('Province')}
        model = SchoolInfo
        fields = '__all__'
        widgets = {
            'content': SummernoteWidget(attrs={'summernote': {'toolbar': [
                ['style', ['style']],
                ['font', ['bold', 'underline', 'clear']],
                ['fontname', ['fontname']],
                ['color', ['forecolor', 'backcolor']],
                ['para', ['ul', 'ol', 'paragraph']],
                ['table', ['table']],
                ['insert', ['link', 'picture', 'video']],
                ['view', ['fullscreen', 'codeview', 'help']],
            ]}}),
            
        }

    def clean_school_phone(self):
        school_phone = self.cleaned_data.get('school_phone')
        matches = re.findall(r'^09\d{8}$', school_phone)
        if not matches:
            raise forms.ValidationError(_('Please enter a valid phone number'))
        return school_phone


class MainArticleForm(forms.ModelForm):
    class Meta:
        labels = {'image':_('Image'),
                  'title':_('Title'),
                  'english_title':_('English Title'),
                  'description':_('Description'),
                  'english_desc':_('English Description')}
        model = MainArticle
        fields = ['title','english_title','description','english_desc','image']
    
    def clean_english_title(self):
        english_title = self.cleaned_data.get('english_title')
        if  english_title:
            if not re.findall('^[a-zA-Z\s]+$', english_title):
                raise forms.ValidationError(
                    _("This field must have just english letters"))
        return english_title