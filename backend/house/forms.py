from django import forms
from .models import *

PRICE = [
    ('0', 'Less than 20 lakhs '),
    ('1', '21-40 lakhs'),
    ('2', '41-60 lakhs'),
    ('3', '61-80 lakhs'),
    ('4', '81-99 lakhs'),
    ('5', 'More than 1 crore')
]

class SellerPostForm(forms.ModelForm):
    price = forms.ChoiceField(choices = PRICE, widget=forms.RadioSelect)

    class Meta:
        model = SellerPost
        fields = '__all__'

class BuyerPostForm(forms.ModelForm):
    price = forms.ChoiceField(choices = PRICE, widget=forms.RadioSelect)

    class Meta:
        model = BuyerPost
        fields = '__all__'

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')
    class Meta:
        model = Image
        fields = ('image',)

class AddFacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields='__all__'