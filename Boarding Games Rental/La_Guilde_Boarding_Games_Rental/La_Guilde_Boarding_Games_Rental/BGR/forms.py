from django import forms
from django.forms import ModelForm
from .models import User


class Form(forms.Form):
    def __init__(self, *args, **kwargs):
        super(Form, self).__init__(*args, **kwargs)
