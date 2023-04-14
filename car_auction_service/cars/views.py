import folium
import geocoder
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.urls import reverse, reverse_lazy

from users.models import UserProfile
from .filters import CarAdvertSearchFilter
from .forms import CarAdvertAddForm, ImageForm
from .models import CarAdvert, CarImage


def cars_list(request):
    """
    Display a list of all cars advertisements in form of filter to make available operation of filtering.

    **Context**

    ''cars''
        An instance of FilterSet :django_filters: 'cars.CarAdvertSearchFilter',
        containing instances of :model: 'cars.CarAdvert'.

    **Template**

    :template: 'cars/cars_main.html'
    """
    car_adverts = CarAdvert.objects.all()
    car_adverts_filter = CarAdvertSearchFilter(request.GET, queryset=car_adverts)
    context = {'car_adverts': car_adverts_filter}
    return render(request, 'cars/cars_main.html', context)


def car_advert_detail(request, pk):
    """
    Display an individual :model: 'cars.CarAdvert'.

    **Context**

    ''cars''
        An instance of :model: 'cars.CarAdvert'.
    ''car_images''
        A list of instances of :model: 'cars.CarImage'.
    ''cars_maps''
        A string representation of instance of :model: 'folium.Map'


    **Template**

    :template: 'cars/car_detail.html'
    """
    car_advert = get_object_or_404(CarAdvert, pk=pk)
    car_images = reversed(get_list_or_404(CarImage, car_advert=car_advert))

    # Adding map component
    # Getting location from car model
    get_car_location = car_advert.location
    location_values = geocoder.osm(f'{get_car_location}, Poland')
    # Creating Map Object
    cars_map = folium.Map(location=location_values.latlng, zoom_start=8)
    # Adding map marker
    folium.Marker(location_values.latlng, tooltip=get_car_location, popup=car_advert).add_to(cars_map)
    # Getting HTML representation of Map Object
    cars_map = cars_map._repr_html_()
    context = {
        'car_advert': car_advert,
        'car_images': car_images,
        'cars_map': cars_map
    }

    return render(request, 'cars/car_detail.html', context)


@login_required(login_url='/users/accounts/login')
def car_advert_delete(request, pk):
    """
    Delete a single instance of :model: 'cars.CarAdvert'.

    **Template**

    :template: 'cars/car_detail.html'
    """
    car_advert = get_object_or_404(CarAdvert, pk=pk)
    car_advert.delete()
    messages.add_message(request, messages.INFO, 'Car was deleted')
    return redirect('/')


@login_required(login_url='/users/accounts/login')
def delete_car_image(request, car_advert_id, image_id):
    """
    Delete a single instance of :model: 'cars.CarImage'.

    **Template**

    :template: 'cars/car_edit2.html'
    """
    car_advert = get_object_or_404(CarAdvert, pk=car_advert_id)
    car_image = get_object_or_404(CarImage, pk=image_id, car_advert=car_advert)

    if request.method == 'POST':
        car_image.delete()
    if len(car_advert.get_all_images()) == 0:
        CarImage.objects.create(car_advert=car_advert, image='images/no_car_image.png')

    messages.add_message(request, messages.INFO, 'Car image was deleted')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/users/accounts/login')
def car_image_set_main(request, car_advert_id, image_id):
    """
    Delete a single instance of :model: 'cars.CarImage'.

    **Template**

    :template: 'cars/car_edit2.html'
    """
    car_advert = get_object_or_404(CarAdvert, pk=car_advert_id)
    car_image = get_object_or_404(CarImage, pk=image_id, car_advert=car_advert)
    car_images = car_advert.carimage_set.all()
    if request.method == 'POST':
        if len(car_images) > 1:
            first_image = car_images.first()
            first_image_id = first_image.id
            car_image.id = first_image_id
            first_image.id = image_id

            first_image.save()
            car_image.save()
            car_advert.save()

    messages.add_message(request, messages.INFO, 'Image was set as main')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required(login_url='/users/accounts/login')
def car_advert_observe(request, pk):
    """
    Add single instance of :model: 'cars.CarAdvert' to observed filed
    of :model: 'users.UserProfile'

    **Template**

    :template: 'cars/car_detail.html'
    """
    car_advert = get_object_or_404(CarAdvert, pk=pk)
    user_profile = get_object_or_404(UserProfile, user=request.user)
    cars_observed = user_profile.cars_observed.all()

    if car_advert not in cars_observed:
        user_profile.cars_observed.add(car_advert)
        car_advert.users_observing.add(request.user)
        messages.success(request, 'Car added to observed')
    else:
        user_profile.cars_observed.remove(car_advert)
        car_advert.users_observing.remove(request.user)
        messages.success(request, 'Car removed from observed')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# rozbić dashboard
@login_required(login_url='/users/accounts/login')
def dashboard(request):
    """
    Display user-specific view of functionalities.
    Display a list of all car advertisements added by user in the form of filter to make available operation of filtering.
    Display a list of car advertisements that are observed by the user.
    Adding new cars to the database.

    **Context**

    ''cars''
        An instance of :model: 'cars.CarAdvert'.
    ''car_add_form''
        An instance of :form: 'cars.CarAdvertAddForm'
    ''images_add_form''
        An instance of :filter: 'cars.ImageForm'
    ''user_profile''
        An instance of :model: 'users.UserProfile'


    **Template**

    :template: 'cars/user_dashboard.html'
    """
    car_adverts = CarAdvert.objects.filter(owner=request.user)
    car_adverts = CarAdvertSearchFilter(request.GET, queryset=car_adverts)
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        car_advert_add_form = CarAdvertAddForm(request.POST)
        images_add_form = ImageForm(request.POST, request.FILES)
        if car_advert_add_form.is_valid() and images_add_form.is_valid():

            # create car instance
            car_advert_instance = car_advert_add_form.save(commit=False)
            print(f'---------------- car_advert_add_form')
            print(car_advert_add_form)
            car_advert_instance.owner = request.user
            car_advert_instance.save()
            print(f'---------------- car_advert_instance')
            print(car_advert_instance)
            print(f'----------------type(car_advert_instance)')
            print(type(car_advert_instance))

            # create car images as being related to car object
            images = request.FILES.getlist('image')
            for car_image in images:
                CarImage.objects.create(car_advert=car_advert_instance, image=car_image)
            messages.add_message(request, messages.INFO, 'Car added')
            # Form with no data after adding a car
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            print(car_advert_add_form.errors)
            messages.add_message(request, messages.INFO, "Failed to add a car")
    else:
        car_advert_add_form = CarAdvertAddForm()
        images_add_form = ImageForm()

    context = {'car_adverts': car_adverts,
               'car_advert_add_form': car_advert_add_form,
               'images_add_form': images_add_form,
               'user_profile': user_profile
               }
    return render(request, 'cars/user_dashboard.html', context)


@login_required(login_url='/users/accounts/login')
def car_advert_edit(request, pk):
    """
    Allows user to edit car details and images.

    **Context**

    ''car''
        An instance of :model: 'cars.CarAdvert'.
    ''car_add_form''
        An instance of :form: 'cars.CarAdvertAddForm'
    ''images_add_form''
        An instance of :filter: 'cars.ImageForm'
    ''user_profile''
        An instance of :model: 'users.UserProfile'


    **Template**

    :template: 'cars/user_dashboard.html'
    """
    car_advert = get_object_or_404(CarAdvert, pk=pk)
    car_image_default = CarImage.objects.filter(car_advert=car_advert).first()

    if request.method == 'POST':
        car_advert_edit_form = CarAdvertAddForm(request.POST, instance=car_advert)
        images_edit_form = ImageForm(request.POST, request.FILES)
        if car_advert_edit_form.is_valid() and images_edit_form.is_valid():

            # create car instance
            car_advert_instance = car_advert_edit_form.save(commit=False)
            car_advert_instance.owner = request.user
            car_advert_instance.save()

            # deleting default car image
            images_empty = len(request.FILES.getlist('image'))
            # if there is car image object and it's image is default and there are added images through form
            # deleting default image only when images added are added through form
            if car_image_default is not None and car_image_default.image == 'images/no_car_image.png' and images_empty != 0:
                car_image_default.delete()

            # create car images as being related to car object
            images = request.FILES.getlist('image')

            for car_image in images:
                CarImage.objects.create(car=car_advert_instance, image=car_image)
            messages.add_message(request, messages.INFO, 'Car modified')
            # Form with no data after adding a car
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.add_message(request, messages.INFO, "Failed to modify a car")
    else:
        car_edit_form = CarAdvertAddForm(instance=car_advert)
        images_add_form = ImageForm()

    context = {'car_advert': car_advert,
               'car_advert_edit_form': car_advert_edit_form,
               'images_add_form': images_add_form
               }
    return render(request, 'cars/car_edit2.html', context)