"""car_auctions helper functionalities"""
from decimal import Decimal

from .models import CarAdvert


def similar_cars(request, pk):
    similar_car_ads = CarAdvert.objects.filter(Q(brand=car_advert.brand) | Q(model=car_advert.model) | Q(price__range=[car_advert.price*Decimal(0.8), car_advert.price*Decimal(1.2)]))[:5]