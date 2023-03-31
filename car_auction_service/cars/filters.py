import django_filters
from django.forms.widgets import TextInput

from .models import Car


class CarSearchFilter(django_filters.FilterSet):
    """Search filter form class for cars queryset."""
    brand = django_filters.CharFilter(lookup_expr='icontains', widget=TextInput(attrs={'placeholder': 'Volvo'}))
    model = django_filters.CharFilter(lookup_expr='icontains', widget=TextInput(attrs={'placeholder': 'V60'}))
    location = django_filters.CharFilter(lookup_expr='icontains', widget=TextInput(attrs={'placeholder': 'Wrocław'}))
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte', widget=TextInput(attrs={'placeholder': 10000}))
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte', widget=TextInput(attrs={'placeholder': 50000}))


    class Meta:
        """Metadata class."""
        model = Car
        fields = ['brand', 'model','location', 'min_price', 'max_price']
