from django import forms
from .models import *

class AddJobTypeForm(forms.ModelForm):
    class Meta:
        model = JobType
        fields = '__all__'

