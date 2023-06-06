"""car_auctions helper functionalities"""
from decimal import Decimal

from django.db.models import Q

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

from .models import CarAdvert

def get_similar_cars(car_advert: object) -> list:
    """
    Return list of similar car adverts to the given car.

    :param car_advert: Object of CarAdvert class.
    :type car_advert: object
    :return: list of the similar objects of CarAdvert class
    :rtype: list
    """
    price_range = 100
    similar_car_ads = []
    for percent in range(1, price_range + 1):

        # get minimal price range for given percentage
        price_min = car_advert.price * (1 - percent * Decimal(0.01))

        # get maximal price range for a given percentage
        price_max = car_advert.price * (1 + percent * Decimal(0.01))

        # get 5 car adverts objects filtered by a price range of price_min and price max, by a car brand and by excluding default car.
        filtered_car_adverts = CarAdvert.objects.filter(~Q(id=car_advert.id) & Q(brand=car_advert.brand) & Q(price__gte=price_min, price__lte=price_max))

        # check if car advert is not already in the list of gathered car adverts and if car advert is still valid.
        for car_advert in filtered_car_adverts:
            if car_advert not in similar_car_ads and car_advert.is_valid:
                similar_car_ads.append(car_advert)

                # if number of the car adverts added to the lsit is equal to 5, break the loop of adding a car to the list
                if len(similar_car_ads) == 5:
                    break

        # if number of the car adverts added to the list is equal to 5, break the loop of adding a car to the list
        if len(similar_car_ads) == 5:
            break

    return similar_car_ads


def get_user_location(ip_address, attempt=1, max_attempts=200):
    """

    :param ip_address: Provided ip_address
    :type ip_address:
    :return:
    :rtype:
    """

    geolocator = Nominatim(user_agent='myapp')
    try:
        location = geolocator.geocode(ip_address)
        if location:
            return location.address
        else:
            return None
    except GeocoderTimedOut:
        if attempt <= max_attempts:
            return get_user_location(ip_address, attempt=attempt+1)
        raise
