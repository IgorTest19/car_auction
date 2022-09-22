from django.shortcuts import render, get_object_or_404
from .models import Car

# Create your views here.


def cars_list(request):
    cars = Car.objects.all()
    return render(request,
                  'cars/cars_list.html',
                  {'cars': cars})


def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'cars/car_detail.html', {'car':car})