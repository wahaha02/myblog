from django import forms
from myblog.blog.models import Media

class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ('title', 'image')
