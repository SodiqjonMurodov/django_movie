from django import forms
from .models import Comments, Movie
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


class CommentForm(forms.ModelForm):
    """Comment Form"""

    class Meta:
        model = Comments
        fields = ('name', 'text', 'email')
