"""car_auctions URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import views

app_name = 'car_auctions'

urlpatterns = [
    path('', views.cars_list, name='cars_main'),
    path('car_advert/<int:pk>', views.car_advert_detail, name='car_advert_detail'),
    path('car_advert/<int:pk>/car_advert_edit', views.car_advert_edit, name='car_advert_edit'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('cars_observed', views.cars_observed, name='cars_observed'),
    path('cars_history', views.car_adverts_viewed, name='car_adverts_viewed'),
    path('car_advert_add', views.car_advert_add, name='car_advert_add'),
    path('car_advert_data', views.car_adavert_data, name='car_advert_data'),
    path('car_advert/<int:pk>/delete', views.car_advert_delete, name='car_advert_delete'),
    path('car_advert/<int:pk>/car_advert_observe', views.car_advert_observe, name='car_advert_observe'),
    path('car_advert/<int:car_advert_id>/delete_car_image//<int:image_id>', views.delete_car_image, name='delete_car_image'),
    path('car_advert/<int:car_advert_id>/car_image_set_main//<int:image_id>', views.car_image_set_main, name='car_image_set_main')
]
