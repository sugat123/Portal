from django import forms
from .models import *

class AddJobTypeForm(forms.ModelForm):
    class Meta:
        model = JobType
        fields = '__all__'
        

class AddSkillTypeForm(forms.ModelForm):
    class Meta:
        model = Skills
        fields = '__all__'


