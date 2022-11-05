from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Car
from .forms import CarAddForm
from .filters import CarSearchFilter

# Create your views here.


def cars_list(request):
    # getting all cars
    cars = Car.objects.all()
    print("---------------------cars object type")
    print(type(cars))
    print(cars)

    # creating form for adding cars
    print("-----1---request.method is")
    print(request.method)

    if request.method == 'POST':
        print("-----2-----request.method == POST")
        print(request.method)
        print("------3--------data=request.POST")
        print(request.POST)
        car_add_form = CarAddForm(data=request.POST)
        print("------4--------car_add_form")
        print(car_add_form)
        if car_add_form.is_valid():
            print("-----5-------DID SAVE")
            car_add_form.save()
            car_add_form = CarAddForm()
            return render(request, 'cars/cars_list.html', {'cars': cars,
                                                           'car_add_form': car_add_form})
    else:
        car_add_form = CarAddForm()

    # if request.method == 'GET':
    cars = CarSearchFilter(request.GET, queryset=cars)
    print("--------------type of cars when filtered")
    print(type(cars))
    print(cars)
    # car_search_form = CarSearchForm()
    # query = None
    # if 'query' in request.GET:
    #     car_search_form = CarSearchForm(data=request.GET)
    #     if car_search_form.is_valid():
    #         query = car_search_form.cleaned_data['query']
    #         cars = Cars.objects.annotate(search)
    #         # car_search_form.save()
    # else:
    #     car_search_form = CarSearchForm()

    return render(request, 'cars/cars_list.html', {'cars': cars,
                                                   'car_add_form':car_add_form})


def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'cars/car_detail.html', {'car':car})

@login.required
def dashboard(request):
    cars = Car.objects.all()
    # cars = CarSearchFilter(request.GET, queryset=cars)
    if request.method == 'POST':
        car_add_form = CarAddForm(data=request.POST)
        if car_add_form.is_valid():
            car = car_add_form.save(commit=False)
            car.owner = request.user
            car_add_form.save()
            # return render(request, 'cars/car_add.html')
    else:
        car_add_form = CarAddForm()

    return render(request, 'cars/user_dashboard.html', {'cars': cars,
                                                         'car_add_form': car_add_form})