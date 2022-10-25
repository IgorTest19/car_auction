from django.shortcuts import render, get_object_or_404
from .models import Car
from .forms import CarForm

# Create your views here.


def cars_list(request):
    # getting all cars
    cars = Car.objects.all()

    # creating form for adding cars
    print("-----1---request.method is")
    print(request.method)

    if request.method == 'POST':
        print("-----2-----request.method == POST")
        print(request.method)
        print("------3--------data=request.POST")
        print(request.POST)
        car_add_form = CarForm(data=request.POST)
        print("------4--------car_add_form")
        print(car_add_form)
        if car_add_form.is_valid():
            print("-----5-------DID SAVE")
            car_add_form.save()
    else:
        car_add_form = CarForm()

    return render(request,
                  'cars/cars_list.html',
                  {'cars': cars,
                  'car_add_form':car_add_form})


def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'cars/car_detail.html', {'car':car})