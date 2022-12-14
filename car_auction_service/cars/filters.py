from django.forms.widgets import TextInput
from .models import Car
import django_filters


class CarSearchFilter(django_filters.FilterSet):
    brand = django_filters.CharFilter(lookup_expr='icontains', widget=TextInput(attrs={'placeholder': 'Volvo'}))
    model = django_filters.CharFilter(lookup_expr='icontains', widget=TextInput(attrs={'placeholder': 'V60'}))

    class Meta:
        model = Car
        fields = ['brand', 'model']
