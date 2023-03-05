import django_filters
from django.forms.widgets import TextInput

from .models import Car


class CarSearchFilter(django_filters.FilterSet):
    """Search filter form class for cars queryset."""
    brand = django_filters.CharFilter(lookup_expr='icontains', widget=TextInput(attrs={'placeholder': 'Volvo'}))
    model = django_filters.CharFilter(lookup_expr='icontains', widget=TextInput(attrs={'placeholder': 'V60'}))
    location = django_filters.CharFilter(lookup_expr='icontains', widget=TextInput(attrs={'placeholder': 'Wrocław'}))
    price = django_filters.NumericRangeFilter(widget=TextInput(attrs={'placeholder': '50 000'}))

    class Meta:
        """Metadata class."""
        model = Car
        fields = ['brand', 'model','location', 'price']
