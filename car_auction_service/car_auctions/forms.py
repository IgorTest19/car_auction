from django import forms

from .models import CarAdvert, CarImage


class CarAdvertAddForm(forms.ModelForm):
    """Form class for adding a new car."""

    class Meta:
        """Metadata class."""

        model = CarAdvert
        # fields = ['brand', 'model', 'year', 'location', 'price', 'fuel_type', 'engine_capacity']
        fields = [
            "brand",
            "model",
            "year",
            "location",
            "price",
            "currency",
            "price_type",
            "fuel_type",
            "engine_capacity",
            "description",
        ]


class ImageForm(forms.ModelForm):
    """Form class for adding car's images."""

    image = forms.ImageField(
        label="Image",
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        required=False,
    )

    class Meta:
        """Metadata class."""

        model = CarImage
        fields = ["image"]
