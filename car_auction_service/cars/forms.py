from django import forms

from .models import Car, CarImage


class CarAddForm(forms.ModelForm):
    """Form class for adding a new car."""
    class Meta:
        """Metadata class."""
        model = Car
        fields = ['brand', 'model', 'year','location']


class ImageForm(forms.ModelForm):
    """Form class for adding car's images."""
    image = forms.ImageField(
        label='Image',
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
    )

    class Meta:
        """Metadata class."""
        model = CarImage
        fields = ["image"]
