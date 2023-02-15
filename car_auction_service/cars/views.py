import folium
import geocoder
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

from users.models import UserProfile
from .filters import CarSearchFilter
from .forms import CarAddForm, ImageForm
from .models import Car, CarImage


def cars_list(request):
    """
    Display list of all cars in form of filter to make available operation of filtering.

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
    car = get_object_or_404(Car, pk=pk)
    car_images = reversed(get_list_or_404(CarImage, car=car))
    # Adding map component
    # Getting location from car model
    get_car_location = car.location
    location_values = geocoder.osm(f'{get_car_location},Poland')
    print(f'-------- {location_values.latlng}')
    # Creating Map Object
    cars_map = folium.Map(location=[52, 20], zoom_start=6)
    # Adding map marker
    folium.Marker(location_values.latlng, tooltip=get_car_location, popup=car).add_to(cars_map)
    # Getting HTML representation of Map Object
    cars_map = cars_map._repr_html_()
    return render(request, 'cars/car_detail.html', {'car': car,
                                                    'car_images': car_images,
                                                    'cars_map': cars_map})


@login_required(login_url='/users/accounts/login')
def car_delete(request, pk):
    car = get_object_or_404(Car, pk=pk)
    car.delete()
    return redirect('cars/user_dashboard.html')


@login_required(login_url='/users/accounts/login')
def car_observe(request, pk):
    car = get_object_or_404(Car, pk=pk)
    user_profile = UserProfile.objects.get(user=request.user.id)
    user_profile.cars_observed.add(car)
    user_profile.save()
    car.users_observing.add(request.user.id)
    car.save()
    print("-----------car.users_observing")
    print(car.users_observing)
    return redirect('cars/user_dashboard.html')


# rozbić dashboard
@login_required(login_url='/users/accounts/login')
def dashboard(request):
    cars = Car.objects.filter(owner=request.user)
    cars = CarSearchFilter(request.GET, queryset=cars)
    user_profile = UserProfile.objects.get(user=request.user)
    car_add_form = CarAddForm()
    images_add_form = ImageForm()
    if request.method == 'POST':
        car_add_form = CarAddForm(request.POST)
        images_add_form = ImageForm(request.POST, request.FILES)
        images = request.FILES.getlist('image')
        if car_add_form.is_valid() and images_add_form.is_valid():
            brand = car_add_form.cleaned_data['brand']
            model = car_add_form.cleaned_data['model']
            year = car_add_form.cleaned_data['year']
            location = car_add_form.cleaned_data['location']
            car_instance = Car.objects.create(
                brand=brand, model=model, year=year, location=location, owner=request.user)
            for car_image in images:
                CarImage.objects.create(car=car_instance, image=car_image)
            messages.success(request, "Adding car was successful")
            car_add_form = CarAddForm()
        else:
            print(car_add_form.errors)
            messages.error(request, "Failed to add a car")
    else:
        car_add_form = CarAddForm()
        images_add_form = ImageForm()

    return render(request,
                  'cars/user_dashboard.html',
                  {'cars': cars,
                   'car_add_form': car_add_form,
                   'images_add_form': images_add_form,
                   'user_profile': user_profile})
