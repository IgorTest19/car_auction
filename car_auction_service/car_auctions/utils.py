"""car_auctions helper functionalities"""
from decimal import Decimal

from django.db.models import Q
from .models import CarAdvert

# TODO: dodać warnek (zawsze) sprawdzania is_valid.

# def get_similar_cars(car_advert):
#     price_range = 100
#     car_ads_by_price = []
#
#     print(f'------------ car_advert price: {car_advert.price}')
#     for percent in range(1, price_range + 1):
#         print(f'--------- percent: {percent}, length of the car_ads_by_price: {len(car_ads_by_price)})')
#         # 80000 * (1 - 1) * 0,001
#         print(
#                 f'------------ car_advert_prices range: {car_advert.price * (1 - percent * Decimal(0.01))} - {car_advert.price * (1 + percent * Decimal(0.01))}')
#         print(
#                 f'------------ car prices percentage range: {car_advert.price * (1 - percent * Decimal(0.01))} - {car_advert.price * (1 + percent * Decimal(0.01))}')
#         car_ads_by_price += CarAdvert.objects.filter(Q(brand=car_advert.brand) | Q(price__gte=car_advert.price * (1 - percent * Decimal(0.01)), price__lte=car_advert.price * (1 + percent * Decimal(0.01))))[:5]
#         if len(car_ads_by_price) == 5:
#             return car_ads_by_price
#
#     print(f'---------------- car_ads_by_price')
#     print(car_ads_by_price)
#     same_price_car_ads = CarAdvert.objects.filter(Q(brand=car_advert.brand) | Q(price=car_advert.price))[:5]
#     if same_price_car_ads:
#         return same_price_car_ads
#     return car_ads_by_price



# def get_similar_cars(car_advert):
#     price_range = 100
#     car_ads_by_price = []
#
#     print(f'------------ car_advert price: {car_advert.price}, car_advert.brand: {car_advert.brand}')
#     for percent in range(1, price_range + 1):
#         print(f'--------- percent: {percent}, length of the car_ads_by_price: {len(car_ads_by_price)})')
#         # 80000 * (1 - 1) * 0,001
#         print(
#                 f'------------ car_advert_prices range: {car_advert.price * (1 - percent * Decimal(0.01))} - {car_advert.price * (1 + percent * Decimal(0.01))}')
#         print(
#                 f'------------ car prices percentage range: {car_advert.price * (1 - percent * Decimal(0.01))} - {car_advert.price * (1 + percent * Decimal(0.01))}')
#         car_ads_by_price += CarAdvert.objects.filter(~Q(id=car_advert.id) & Q(brand=car_advert.brand) & Q(price__gte=car_advert.price * (1 - percent * Decimal(0.01)), price__lte=car_advert.price * (1 + percent * Decimal(0.01))))[:5]
#
#         if len(car_ads_by_price) == 5:
#             # return car_ads_by_price
#             break
#     print(f'------------ car_ads_by_price: {car_ads_by_price}')
#     for car in car_ads_by_price:
#         print(car.price)
#
#     same_price_car_ads = CarAdvert.objects.filter(Q(brand=car_advert.brand) | Q(price=car_advert.price))[:5]
#     if same_price_car_ads:
#         return same_price_car_ads
#     return car_ads_by_price


def get_similar_cars(car_advert):
    price_range = 100
    similar_car_ads = []
    for percent in range(1, price_range + 1):

        print(f'-----iteration/percent {percent}')
        print(f'-----similar_car_ads_at_the_beginning {similar_car_ads}')
        # get minimal price range for given percentage
        price_min = car_advert.price * (1 - percent * Decimal(0.01))

        # get maximal price range for a given percentage
        price_max = car_advert.price * (1 + percent * Decimal(0.01))

        # get 5 car adverts objects filtered by a price range of price_min and price max, by a car brand and by excluding default car.
        filtered_car_adverts = CarAdvert.objects.filter(~Q(id=car_advert.id) & Q(brand=car_advert.brand) & Q(price__gte=price_min, price__lte=price_max))

        print(f'------- filtered_car_adverts: {filtered_car_adverts}')

        # exclude filtered car adverts if they are already added to the list

        # filtered_car_adverts_clean = filtered_car_adverts.exclude(id__in=[car.id for car in similar_car_ads])

        # filtered_car_adverts_clean = filtered_car_adverts_clean.exclude(id=car_advert.id)
        print(f'----- for check')
        for car_advert in filtered_car_adverts:
            print(f'----car_advert_id: {car_advert}')
            print(f'----- similar_cars: {similar_car_ads}')
            if car_advert not in similar_car_ads and car_advert.is_valid:
                similar_car_ads.append(car_advert)

                if len(similar_car_ads) == 5:
                    print(f'-------len(similar_car_ads): {len(similar_car_ads)}')
                    print(f'------ {similar_car_ads}')
                    break



        # similar_car_ads += list(filtered_car_adverts_clean)

        if len(similar_car_ads) == 5:
            print(f'-------len(similar_car_ads): {len(similar_car_ads)}')
            print(f'------ {similar_car_ads}')
            break
            # return similar_car_ads


    return similar_car_ads


# from django.db.models import Q
# from .models import Car
#
# brand = 'Toyota'
# base_price = 10000
# percentage_increase = 0.01
# num_iterations = 100
#
# query = Q(brand=brand)
# cars = []
#
# added_car_ids = set()
#
# for i in range(num_iterations):
#     min_price = base_price * (1 + i * percentage_increase)
#     max_price = base_price * (1 + (i + 1) * percentage_increase)
#     query &= Q(price__range=(min_price, max_price))
#     filtered_cars = Car.objects.filter(query)[:5]
#
#     for car in filtered_cars:
#         if car.id not in added_car_ids:
#             cars.append(car)
#             added_car_ids.add(car.id)
