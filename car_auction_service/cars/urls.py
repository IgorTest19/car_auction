"""cars URL Configuration

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

app_name = 'cars'

urlpatterns = [
    path('', views.cars_list, name='cars_main'),
    path('car/<int:pk>', views.car_detail, name='car_detail'),
    path('car/<int:pk>/car_edit', views.car_edit, name='car_edit'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('car/<int:pk>/delete', views.car_delete, name='car_delete'),
    path('car/<int:pk>/car_observe', views.car_observe, name='car_observe'),
    path('car/<int:car_id>/delete_car_image//<int:image_id>', views.delete_car_image, name='delete_car_image')
]
