from .models import Car
import django_filters

class CarSearchFilter(django_filters.FilterSet):
    class Meta:
        model = Car
        fields = {
            'title': ['icontains'],
            'body': ['icontains'],
        }
