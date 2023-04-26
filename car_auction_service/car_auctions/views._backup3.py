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
    Display a list of all car_auctions in form of filter to make available operation of filtering.

    **Context**

    ''car_auctions''
        An instance of FilterSet :django_filters: 'car_auctions.CarSearchFilter',
        containing instances of :model: 'car_auctions.Car'.

    **Template**

    :template: 'car_auctions/cars_main.html'
    """
    cars = Car.objects.all()
    cars = CarSearchFilter(request.GET, queryset=cars)
    context = {'car_auctions': cars}
    return render(request, 'car_auctions/cars_main.html', context)


def car_detail(request, pk):
    """
    Display an individual :model: 'car_auctions.Car'.

    **Context**

    ''car_auctions''
        An instance of :model: 'car_auctions.Car'.
    ''car_images''
        A list of instances of :model: 'car_auctions.CarImage'.
    ''cars_maps''
        A string representation of instance of :model: 'folium.Map'


    **Template**

    :template: 'car_auctions/car_detail.html'
    """
    car = get_object_or_404(Car, pk=pk)
    car_images = reversed(get_list_or_404(CarImage, car=car))
    # Adding map component
    # Getting location from car model
    get_car_location = car.location
    location_values = geocoder.osm(f'{get_car_location}, Poland')
    print(f'-------- {location_values.latlng}')
    # Creating Map Object
    cars_map = folium.Map(location=[52, 20], zoom_start=6)
    # Adding map marker
    folium.Marker(location_values.latlng, tooltip=get_car_location, popup=car).add_to(cars_map)
    # Getting HTML representation of Map Object
    cars_map = cars_map._repr_html_()
    context = {
        'car': car,
        'car_images': car_images,
        'cars_map': cars_map
    }
    return render(request, 'car_auctions/car_detail.html', context)


@login_required(login_url='/users/accounts/login')
def car_delete(request, pk):
    """
    Delete a single instance of :model: 'car_auctions.Car'.

    **Template**

    :template: 'car_auctions/car_detail.html'
    """
    car = get_object_or_404(Car, pk=pk)
    car.delete()
    return redirect('/')


@login_required(login_url='/users/accounts/login')
def car_observe(request, pk):
    """
    Add single instance of :model: 'car_auctions.Car' to observed filed
    of :model: 'users.UserProfile'

    **Template**

    :template: 'car_auctions/user_dashboard.html'
    """
    car = get_object_or_404(Car, pk=pk)
    print(car)
    user_profile = UserProfile.objects.get(user=request.user.id)
    cars_ob = user_profile.cars_observed.all()
    if car not in cars_ob:
        user_profile.cars_observed.add(car)
        user_profile.save()
        car.users_observing.add(request.user.id)
        car.save()
    else:
        user_profile.cars_observed.remove(car)
        user_profile.save()
        car.users_observing.remove(request.user.id)
        car.save()

    # context = {
    #     'car': car,
    #     'car_images': car_images,
    #     'cars_map': cars_map
    # }
    # return redirect(request.path)
    # return HttpResponseRedirect(request.path_info)
    # return redirect(reverse_lazy('car_auctions:car_detail'))
    # return render(request, 'car_auctions/car_detail.html', context)
    # return redirect('car_auctions/car_detail.html')
    # return redirect('/')
    # return HttpResponse(status=204)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# rozbić dashboard
@login_required(login_url='/users/accounts/login')
def dashboard(request):
    """
    Display user-specific view of functionalities.
    Display a list of all car_auctions added by user in the form of filter to make available operation of filtering.
    Display a list of car_auctions that are observed by the user.
    Adding new car_auctions to the database.

    **Context**

    ''car_auctions''
        An instance of :model: 'car_auctions.Car'.
    ''car_add_form''
        An instance of :form: 'car_auctions.CarAddForm'
    ''images_add_form''
        An instance of :filter: 'car_auctions.ImageForm'
    ''user_profile''
        An instance of :model: 'users.UserProfile'


    **Template**

    :template: 'car_auctions/user_dashboard.html'
    """
    cars = Car.objects.filter(owner=request.user)
    cars = CarSearchFilter(request.GET, queryset=cars)
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        car_add_form = CarAddForm(request.POST)
        images_add_form = ImageForm(request.POST, request.FILES)
        images = request.FILES.getlist('image')
        if car_add_form.is_valid() and images_add_form.is_valid():
            brand = car_add_form.cleaned_data['brand']
            model = car_add_form.cleaned_data['model']
            year = car_add_form.cleaned_data['year']
            location = car_add_form.cleaned_data['location']
            # creating car objects based on provided data
            car_instance = Car.objects.create(
                brand=brand, model=model, year=year, location=location, owner=request.user)
            # creating car's images as related to it objects
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

    context = {'car_auctions': cars,
               'car_add_form': car_add_form,
               'images_add_form': images_add_form,
               'user_profile': user_profile}
    return render(request, 'car_auctions/user_dashboard.html', context)
