from django import forms
from .models import *
# from django_quill.forms import QuillFormField

class LogInForm(forms.Form):
    uni_username = forms.CharField()
    password = forms.CharField(label="Password",
        widget=forms.PasswordInput)

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = (
            'title',
            'text',
        )

class EditPostForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = (
            'title',
            'text',
        )
