import folium
import geocoder
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.urls import reverse, reverse_lazy

from users.models import UserProfile
from .filters import CarSearchFilter
from .forms import CarAddForm, ImageForm
from .models import Car, CarImage


def cars_list(request):
    """
    Display a list of all cars in form of filter to make available operation of filtering.

    **Context**

    ''cars''
        An instance of FilterSet :django_filters: 'cars.CarSearchFilter',
        containing instances of :model: 'cars.Car'.

    **Template**

    :template: 'cars/cars_main.html'
    """
    cars = Car.objects.all()
    cars = CarSearchFilter(request.GET, queryset=cars)
    context = {'cars': cars}
    return render(request, 'cars/cars_main.html', context)


def car_detail(request, pk):
    """
    Display an individual :model: 'cars.Car'.

    **Context**

    ''cars''
        An instance of :model: 'cars.Car'.
    ''car_images''
        A list of instances of :model: 'cars.CarImage'.
    ''cars_maps''
        A string representation of instance of :model: 'folium.Map'


    **Template**

    :template: 'cars/car_detail.html'
    """
    car = get_object_or_404(Car, pk=pk)
    car_images = reversed(get_list_or_404(CarImage, car=car))
    # Adding map component
    # Getting location from car model
    get_car_location = car.location
    location_values = geocoder.osm(f'{get_car_location}, Poland')
    print(f'-------- {location_values.latlng}')
    # Creating Map Object
    cars_map = folium.Map(location=location_values.latlng, zoom_start=8)
    # Adding map marker
    folium.Marker(location_values.latlng, tooltip=get_car_location, popup=car).add_to(cars_map)
    # Getting HTML representation of Map Object
    cars_map = cars_map._repr_html_()
    context = {
        'car': car,
        'car_images': car_images,
        'cars_map': cars_map
    }
    return render(request, 'cars/car_detail.html', context)


@login_required(login_url='/users/accounts/login')
def car_delete(request, pk):
    """
    Delete a single instance of :model: 'cars.Car'.

    **Template**

    :template: 'cars/car_detail.html'
    """
    car = get_object_or_404(Car, pk=pk)
    car.delete()
    messages.add_message(request, messages.INFO, 'Car was deleted')
    return redirect('/')


@login_required(login_url='/users/accounts/login')
def car_observe(request, pk):
    """
    Add single instance of :model: 'cars.Car' to observed filed
    of :model: 'users.UserProfile'

    **Template**

    :template: 'cars/user_dashboard.html'
    """
    car = get_object_or_404(Car, pk=pk)
    print(car)
    user_profile = get_object_or_404(UserProfile, user=request.user)
    cars_ob = user_profile.cars_observed.all()
    if car not in cars_ob:
        user_profile.cars_observed.add(car)
        user_profile.save()
        car.users_observing.add(request.user.id)
        car.save()
        messages.add_message(request, messages.INFO, 'Car added to observed')
    else:
        user_profile.cars_observed.remove(car)
        user_profile.save()
        car.users_observing.remove(request.user.id)
        car.save()
        messages.add_message(request, messages.INFO, 'Car removed from observed')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# rozbić dashboard
@login_required(login_url='/users/accounts/login')
def dashboard(request):
    """
    Display user-specific view of functionalities.
    Display a list of all cars added by user in the form of filter to make available operation of filtering.
    Display a list of cars that are observed by the user.
    Adding new cars to the database.

    **Context**

    ''cars''
        An instance of :model: 'cars.Car'.
    ''car_add_form''
        An instance of :form: 'cars.CarAddForm'
    ''images_add_form''
        An instance of :filter: 'cars.ImageForm'
    ''user_profile''
        An instance of :model: 'users.UserProfile'


    **Template**

    :template: 'cars/user_dashboard.html'
    """
    cars = Car.objects.filter(owner=request.user)
    cars = CarSearchFilter(request.GET, queryset=cars)
    user_profile = get_object_or_404(UserProfile, user=request.user)


    if request.method == 'POST':
        car_add_form = CarAddForm(request.POST)
        images_add_form = ImageForm(request.POST, request.FILES)
        images = request.FILES.getlist('image')
        if car_add_form.is_valid() and images_add_form.is_valid():
            # getting all needed data values from the form
            brand = car_add_form.cleaned_data['brand']
            model = car_add_form.cleaned_data['model']
            year = car_add_form.cleaned_data['year']
            location = car_add_form.cleaned_data['location']
            price = car_add_form.cleaned_data['price']
            fuel_type = car_add_form.cleaned_data['fuel_type']
            engine_capacity = car_add_form.cleaned_data['engine_capacity']
            # creating car objects based on provided data
            car_instance = Car.objects.create(
                brand=brand, model=model, year=year, location=location, price=price, fuel_type=fuel_type,
                engine_capacity=engine_capacity, owner=request.user)
            # creating car's images as related to it objects
            for car_image in images:
                CarImage.objects.create(car=car_instance, image=car_image)
            messages.add_message(request, messages.INFO, 'Car added')
            # Form with no data after adding a car
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            print(car_add_form.errors)
            messages.add_message(request, messages.INFO, "Failed to add a car")
    else:
        car_add_form = CarAddForm()
        images_add_form = ImageForm()

    context = {'cars': cars,
               'car_add_form': car_add_form,
               'images_add_form': images_add_form,
               'user_profile': user_profile
               }
    return render(request, 'cars/user_dashboard.html', context)
