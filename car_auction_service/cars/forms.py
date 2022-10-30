from django import forms
from .models import Car

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ('brand', 'model', 'year')

class CarSearchForm(forms.Form):
    query = forms.CharField()