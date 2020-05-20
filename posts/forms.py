from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django.utils.translation import ugettext_lazy as _

from .models import Post


class AddPostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['overview'].widget = forms.Textarea()
        self.fields['content'].widget = SummernoteWidget()
        self.fields['active'].required = False
        self.fields['main_image'].required = False

    class Meta:
        labels = {'title': _('Title'),
                  'overview': _('Overview'),
                  'content': _('Content'),
                  'active': _('Activate'),
                  'main_image': _('Main Image (Optional)')}
        model = Post
        exclude = ['slug', 'author', 'published_date']
