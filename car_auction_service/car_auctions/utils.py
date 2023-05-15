"""car_auctions helper functionalities"""
from decimal import Decimal

from django.db.models import Max, Q
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from .models import CarAdvert, RecentlyViewed



def get_similar_cars(car_advert, recently_viewed):
    # print(f'---- get_similar_cars is working from .utils level')
    # print(f'---- passed car')
    # print(recently_viewed)
    #
    # if CarAdvert.objects.filter(price=car_advert.price):
    #     price = CarAdvert.objects.filter(price=car_advert.price)
    # elif CarAdvert.objects.filter(price__gte=car_advert.price*0.80, price__lte=car_advert.price*1.20)
    #     price = CarAdvert.objects.filter(price__gte=car_advert.price*0.08, price__lte=car_advert.price*1.20)
    # elif CarAdvert.objects.filter(price__gte=car_advert.price*0.80, price__lte=car_advert.price*1.40)
    #
    #
    # # Suggested similar car advertisements
    # similar_car_ads = CarAdvert.objects.filter((Q(brand=car_advert.brand) | Q(model=car_advert.model)) & Q(
    #     price__range=[car_advert.price * Decimal(0.8), car_advert.price * Decimal(1.2)]))[:5]
    # print('-------------------similar car ads')
    # print(similar_car_ads)
    #
    # tested_return = f'returned get_similar_cars car {car}'
    # return tested_return
    pass

def filter_by_price(car_advert):
    max_price = CarAdvert.objects.aggregate(max_price=Max('price'))['max_price']
    print(f'---------- max price: {max_price}')
    price_range = 100

    for percent in range(1, price_range + 1):
        car_ads_by_price = CarAdvert.objects.filter(Q(brand=car_advert.brand) | Q(price__gte=car_advert.price*(1-percent)*Decimal(0.01), price__lte=car_advert.price*(1+percent)*Decimal(0.01)))[:5]

    same_price_car_ads = CarAdvert.objects.filter(Q(brand=car_advert.brand) | Q(price=car_advert.price))[:5]
    if same_price_car_ads:
        return same_price_car_ads
    return car_ads_by_price