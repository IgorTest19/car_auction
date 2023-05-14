"""car_auctions helper functionalities"""
from decimal import Decimal

from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from .models import CarAdvert, RecentlyViewed



def get_similar_cars(car_advert, recently_viewed):
    print(f'---- get_similar_cars is working from .utils level')
    print(f'---- passed car')
    print(recently_viewed)

    if CarAdvert.objects.filter(price=car_advert.price):
        price = CarAdvert.objects.filter(price=car_advert.price)
    elif CarAdvert.objects.filter(price__gte=car_advert.price*0.80, price__lte=car_advert.price*1.20)
        price = CarAdvert.objects.filter(price__gte=car_advert.price*0.08, price__lte=car_advert.price*1.20)
    elif CarAdvert.objects.filter(price__gte=car_advert.price*0.80, price__lte=car_advert.price*1.40)


    # Suggested similar car advertisements
    similar_car_ads = CarAdvert.objects.filter((Q(brand=car_advert.brand) | Q(model=car_advert.model)) & Q(
        price__range=[car_advert.price * Decimal(0.8), car_advert.price * Decimal(1.2)]))[:5]
    print('-------------------similar car ads')
    print(similar_car_ads)

    tested_return = f'returned get_similar_cars car {car}'
    return tested_return

def filter_by_price(car_class, car_obj):
    price_range = 100

    for percent in range(price_range):
        car_ads_by_price = car_class.objects.filter(price__gte=car_obj.price*percent, price_lte=car_obj.price*(percent+1))

    same_price_car_ads = car_class.objects.filter(price=car_obj.price)
    if same_price_car_ads:
        return same_price_car_ads
    return car_ads_by_price