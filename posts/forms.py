from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


from .models import Post


class AddPostForm(forms.ModelForm):
    title = forms.CharField(label=' العنوان')
    overview = forms.CharField(label=' المقدمة', widget=forms.Textarea())
    content = forms.CharField(widget=SummernoteWidget(),
                              label=' المحتوى')
    active = forms.BooleanField(label='تفعيل', required=False)
    main_image = forms.ImageField(
        required=False, label='الصورة الرئيسية (إختياري)')

    class Meta:
        model = Post
        exclude = ['slug', 'author']
