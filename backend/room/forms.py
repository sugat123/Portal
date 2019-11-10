from django import forms
from .models import *

PRICE = [
    ('3000-4000', '3000-4000'),
    ('4000-5000', '4000-5000'),
    ('5000-6000', '5000-6000'),
    ('6000-7000', '6000-7000'),
    ('7000-8000', '7000-8000'),
    ('More than 8000', 'More than 8000')
]


class PostedRoomForm(forms.ModelForm):
    user_type = forms.ChoiceField(choices = PRICE, widget=forms.RadioSelect)

    class Meta:
        model = PostedRoom
        fields = '__all__'

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = '__all__'

class AddFacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = '__all__'