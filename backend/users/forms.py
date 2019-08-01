from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from users.models import *


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False)


class AddUserForm(UserCreationForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email Already Exists')
        return email

    class Meta:
        model = User
        fields = ["email", "password1",
                  "password2"]


class ProfileForm(forms.ModelForm):
    # user_type=forms.ChoiceField(choices = TYPES,widget=forms.RadioSelect())
    class Meta:
        model = Profile
        fields = ('number','user_type')

    def clean_number(self):
        number = self.cleaned_data['number']
        if Profile.objects.filter(number = number).exists():
            raise ValidationError('Phone Number Already Exists')
        return number
