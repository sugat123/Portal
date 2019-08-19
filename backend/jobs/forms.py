from django import forms
from .models import *


class AddJobTypeForm(forms.ModelForm):
    class Meta:
        model = JobType
        fields = '__all__'


class AddSkillForm(forms.ModelForm):
    class Meta:
        model = Skills
        fields = '__all__'


class AddFacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = '__all__'


class AddPostedJobForm(forms.ModelForm):
    class Meta:
        model = PostedJob
        fields = '__all__'


class AddAppliedJobForm(forms.ModelForm):
    class Meta:
        model = AppliedJob
        fields = '__all__'


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
