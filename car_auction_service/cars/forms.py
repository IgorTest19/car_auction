from django import forms
from .models import Car

class CarAddForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ('brand', 'model', 'year')

