from django import forms
from .models import *

PRICE = [
    ('0', '3000-4000'),
    ('1', '4000-5000'),
    ('2', '5000-6000'),
    ('3', '6000-7000'),
    ('4', '7000-8000'),
    ('5', 'More than 8000')
]


class PostedRoomForm(forms.ModelForm):
    price = forms.ChoiceField(choices = PRICE, widget=forms.RadioSelect)

    class Meta:
        model = PostedRoom
        fields = '__all__'

class ImageForm(forms.ModelForm):
    image = forms.ImageField() 

    class Meta:
        model = Image
        fields = ('image',)

class AddFacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = '__all__'

class SearchRoomForm(forms.ModelForm):
    price = forms.ChoiceField(choices = PRICE, widget=forms.RadioSelect)
    class Meta:
        model = SearchedRoom
        fields = '__all__'

