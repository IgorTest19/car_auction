import folium
import geocoder
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
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
    print(f'--------------------------------FIRST IMAGE:  {car.carimage_set.all()[0]}')
    print(f'--------------------------------ALL images:  {car.carimage_set.all()}')
    car_image_first = car.carimage_set.first()
    car_image_last = car.carimage_set.last()
    print(f'--------------------------------FIRST IMAGE: {car_image_first} ')
    print(f'--------------------------------LAST IMAGE: {car_image_last} ')
    # car.carimage_set.first():
    car.carimage_set.first().id, car.carimage_set.last().id = car.carimage_set.last().id, car.carimage_set.first().id
    car.carimage_set.first().save()
    car.carimage_set.last().save()


    first_id = car.carimage_set.first().id
    print(f'---------- first id {first_id}')
    last_id = car.carimage_set.last().id
    print(f'---------- last_id {last_id}')
    car.carimage_set.first().id = last_id
    car.carimage_set.last().id = first_id
    print(f'--------------------------------ALL images:  {car.carimage_set.all()}')
    car.carimage_set.first().save()
    car.carimage_set.last().save()
    print(f'--------------------------------ALL images:  {car.carimage_set.all()}')
    # Get all car images for a car
    car_images = car.carimage_set.all()

    if car_images.exists():
        first_image = car_images.first()
        last_image = car_images.last()

        first_image_id = first_image.id
        first_image.id = last_image.id
        last_image.id = first_image_id

        first_image.save()
        last_image.save()


    # for car_image in car.carimage_set.all():
    #     id = car_image.id
    #     print(f'--- id {id}')
    #     print(f'---car_image: {car_image}')
    #     if car_image.id == 488:
    #         car_image.id = 490
    #         car_image.save()

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
def delete_car_image(request, car_id, image_id):
    """
    Delete a single instance of :model: 'cars.CarImage'.

    **Template**

    :template: 'cars/car_edit2.html'
    """
    car = get_object_or_404(Car, pk=car_id)
    car_image = get_object_or_404(CarImage, pk=image_id, car=car)

    if request.method == 'POST':
        car_image.delete()
    if len(car.get_all_images()) == 0:
        CarImage.objects.create(car=car, image='images/no_car_image.png')
    messages.add_message(request, messages.INFO, 'Car image was deleted')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/users/accounts/login')
def car_image_set_main(request, car_id, image_id):
    """
    Delete a single instance of :model: 'cars.CarImage'.

    **Template**

    :template: 'cars/car_edit2.html'
    """
    car = get_object_or_404(Car, pk=car_id)
    car_image = get_object_or_404(CarImage, pk=image_id, car=car)
    car_images = car.carimage_set.all()
    if request.method == 'POST':
        if len(car_images) > 1:
            first_image = car_images.first()
            first_image_id = first_image.id
            car_image.id = first_image_id
            first_image.id = image_id

            first_image.save()
            car_image.save()
            car.save()

    messages.add_message(request, messages.INFO, 'Image was set as main')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required(login_url='/users/accounts/login')
def car_observe(request, pk):
    """
    Add single instance of :model: 'cars.Car' to observed filed
    of :model: 'users.UserProfile'

    **Template**

    :template: 'cars/car_detail.html'
    """
    car = get_object_or_404(Car, pk=pk)
    user_profile = get_object_or_404(UserProfile, user=request.user)
    cars_observed = user_profile.cars_observed.all()

    if car not in cars_observed:
        user_profile.cars_observed.add(car)
        car.users_observing.add(request.user)
        messages.success(request, 'Car added to observed')
    else:
        user_profile.cars_observed.remove(car)
        car.users_observing.remove(request.user)
        messages.success(request, 'Car removed from observed')

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
        if car_add_form.is_valid() and images_add_form.is_valid():

            # create car instance
            car_instance = car_add_form.save(commit=False)
            car_instance.owner = request.user
            car_instance.save()

            # create car images as being related to car object
            images = request.FILES.getlist('image')
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


@login_required(login_url='/users/accounts/login')
def car_edit(request, pk):
    """
    Allows user to edit car details and images.

    **Context**

    ''car''
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
    car = get_object_or_404(Car, pk=pk)
    car_image_default = CarImage.objects.filter(car=car).first()

    if request.method == 'POST':
        car_edit_form = CarAddForm(request.POST, instance=car)
        images_edit_form = ImageForm(request.POST, request.FILES)
        if car_edit_form.is_valid() and images_edit_form.is_valid():

            # create car instance
            car_instance = car_edit_form.save(commit=False)
            car_instance.owner = request.user
            car_instance.save()

            # deleting default car image
            images_empty = len(request.FILES.getlist('image'))
            # if there is car image object and it's image is default and there are added images through form
            # deleting default image only when images added are added through form
            if car_image_default is not None and car_image_default.image == 'images/no_car_image.png' and images_empty != 0:
                car_image_default.delete()

            # create car images as being related to car object
            images = request.FILES.getlist('image')

            for car_image in images:
                CarImage.objects.create(car=car_instance, image=car_image)
            messages.add_message(request, messages.INFO, 'Car modified')
            # Form with no data after adding a car
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.add_message(request, messages.INFO, "Failed to modify a car")
    else:
        car_edit_form = CarAddForm(instance=car)
        images_add_form = ImageForm()

    context = {'car': car,
               'car_edit_form': car_edit_form,
               'images_add_form': images_add_form
               }
    return render(request, 'cars/car_edit2.html', context)
