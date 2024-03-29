from django import forms
from django.forms import ModelForm
from .models import User


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['email'] = forms.EmailField()
        self.fields['password'] = forms.CharField(
            widget=forms.PasswordInput, min_length=5, max_length=30)
