from django import forms

from .models import Car, CarImage


class CarAddForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'year']


class ImageForm(forms.ModelForm):
    image = forms.ImageField(
        label='Image',
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
    )

    class Meta:
        model = CarImage
        fields = ["image"]
