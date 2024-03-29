from decimal import Decimal

import folium
import geocoder

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.cache import cache_control
from users.models import UserProfile

from .filters import CarAdvertSearchFilter
from .forms import CarAdvertAddForm, ImageForm
from .models import CarAdvert, CarImage, RecentlyViewed
from .utils import get_similar_cars, get_user_location


def cars_list(request):
    """
    Display a list of all cars advertisements in form of filter to make available operation of filtering.

    **Context**

    ''car_adverts''
        An instance of FilterSet :django_filters: 'car_auctions.CarAdvertSearchFilter',
        containing instances of :model: 'car_auctions.CarAdvert'.

    **Template**

    :template: 'car_auctions/cars_main.html'
    """
    car_adverts = CarAdvert.objects.all()
    car_adverts_filter = CarAdvertSearchFilter(request.GET, queryset=car_adverts)
    context = {"car_adverts": car_adverts_filter}
    return render(request, "car_auctions/cars_main.html", context)


@login_required(login_url="/users/accounts/login")
def car_advert_detail(request, pk):
    """
    Display an individual :model: 'car_auctions.CarAdvert'.

    **Context**

    ''car_advert''
        An instance of :model: 'car_auctions.CarAdvert'.
    ''car_images''
        A list of instances of :model: 'car_auctions.CarImage'.
    ''cars_maps''
        A string representation of instance of :model: 'folium.Map'


    **Template**

    :template: 'car_auctions/car_detail.html'
    """
    car_advert = get_object_or_404(CarAdvert, pk=pk)
    car_images = reversed(get_list_or_404(CarImage, car_advert=car_advert))

    # Adding the viewed car advert to the history of viewed car adverts, if it has not been added yet.
    # Otherwise, update the date it was viewed.
    recently_viewed, created = RecentlyViewed.objects.get_or_create(
        user=request.user, car_advert=car_advert
    )
    if not created:
        recently_viewed.viewed_at = timezone.now()
        recently_viewed.save()

    # Adding map component.
    # Getting location from the car model.
    get_car_location = car_advert.location
    location_values = geocoder.osm(f"{get_car_location}, Poland")
    # Creating a Map Object
    cars_map = folium.Map(location=location_values.latlng, zoom_start=8)
    # Adding a map marker
    folium.Marker(
        location_values.latlng, tooltip=get_car_location, popup=car_advert
    ).add_to(cars_map)
    # Getting HTML representation of the Map Object
    cars_map = cars_map._repr_html_()

    # Suggested similar car advertisements
    similar_car_ads = get_similar_cars(car_advert)

    context = {
        "car_advert": car_advert,
        "car_images": car_images,
        "cars_map": cars_map,
        "similar_car_ads": similar_car_ads,
    }

    return render(request, "car_auctions/car_detail.html", context)


@login_required(login_url="/users/accounts/login")
def car_advert_delete(request, pk):
    """
    Delete a single instance of :model: 'car_auctions.CarAdvert'.

    **Template**

    :template: 'car_auctions/car_detail.html'
    """
    car_advert = get_object_or_404(CarAdvert, pk=pk)
    car_advert.delete()
    messages.add_message(request, messages.INFO, "Car was deleted")
    return redirect("/")


@login_required(login_url="/users/accounts/login")
def delete_car_image(request, car_advert_id, image_id):
    """
    Delete a single instance of :model: 'car_auctions.CarImage'.

    **Template**

    :template: 'car_auctions/car_edit2.html'
    """
    car_advert = get_object_or_404(CarAdvert, pk=car_advert_id)
    car_image = get_object_or_404(CarImage, pk=image_id, car_advert=car_advert)

    if request.method == "POST":
        car_image.delete()
    if len(car_advert.get_all_images()) == 0:
        CarImage.objects.create(car_advert=car_advert, image="images/no_car_image.png")

    messages.add_message(request, messages.INFO, "Car image was deleted")

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required(login_url="/users/accounts/login")
def car_image_set_main(request, car_advert_id, image_id):
    """
    Delete a single instance of :model: 'car_auctions.CarImage'.

    **Template**

    :template: 'car_auctions/car_edit2.html'
    """
    car_advert = get_object_or_404(CarAdvert, pk=car_advert_id)
    car_image = get_object_or_404(CarImage, pk=image_id, car_advert=car_advert)
    car_images = car_advert.carimage_set.all()
    if request.method == "POST":
        if len(car_images) > 1:
            first_image = car_images.first()
            first_image_id = first_image.id
            car_image.id = first_image_id
            first_image.id = image_id

            first_image.save()
            car_image.save()
            car_advert.save()

    messages.add_message(request, messages.INFO, "Image was set as main")

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required(login_url="/users/accounts/login")
def car_advert_observe(request, pk):
    """
    Add single instance of :model: 'car_auctions.CarAdvert' to observed filed
    of :model: 'users.UserProfile'

    **Template**

    :template: 'car_auctions/car_detail.html'
    """
    car_advert = get_object_or_404(CarAdvert, pk=pk)
    user_profile = get_object_or_404(UserProfile, user=request.user)
    cars_observed = user_profile.cars_observed.all()

    if car_advert not in cars_observed:
        user_profile.cars_observed.add(car_advert)
        car_advert.users_observing.add(request.user)
        messages.success(request, "Car added to observed")
    else:
        user_profile.cars_observed.remove(car_advert)
        car_advert.users_observing.remove(request.user)
        messages.success(request, "Car removed from observed")

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required(login_url="/users/accounts/login")
def cars_observed(request):
    """
    Display user-specific view of functionalities.
    Display a list of all car advertisements added by user in the form of filter to make available operation of filtering.
    Display a list of car advertisements that are observed by the user.
    Adding new car advert to the database.

    **Context**

    ''car_adverts''
        An instance of :model: 'car_auctions.CarAdvert'.
    ''car_add_form''
        An instance of :form: 'car_auctions.CarAdvertAddForm'
    ''images_add_form''
        An instance of :filter: 'car_auctions.ImageForm'
    ''user_profile''
        An instance of :model: 'users.UserProfile'


    **Template**

    :template: 'car_auctions/user_dashboard.html'
    """

    # Observed cars
    user_profile = get_object_or_404(UserProfile, user=request.user)
    cars_observed = user_profile.cars_observed.all()
    car_adverts = CarAdvertSearchFilter(request.GET, queryset=cars_observed)

    # Adding map component
    #  car_adverts_locations = [car_advert.location for car_advert in user_profile.cars_observed_by_user2()]
    car_adverts_observed = user_profile.cars_observed_by_user2()

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    print(f'----x_forwarded_for: {x_forwarded_for}')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print(f'------ iP IS: {ip}')
    # Getting user location by IP Address
    # user_ip = request.META.get('REMOTE_ADDR')
    # latitude, longitude = get_user_location((user_ip))
    # print(f'-----latitude: {latitude}')
    # print(f'-----longitude: {longitude}')

    # Creating a Map Object based on the revceived location
    # if latitude and longitude:
    #     map = folium.Map(location=[53.8643700, 21.3050700], zoom_start=4)
    # else:
    #     map = folium.Map(location=[53.8643700, 21.3050700], zoom_start=4)
    #
    # Creating a Map Object based on the revceived location
    map = folium.Map(location=[52.12, 19.08], zoom_start=6)

    for car_advert in car_adverts_observed:
        # Getting location values
        location_values = geocoder.osm(f'{car_advert.location}, Poland')
        # Adding a map marker
        folium.Marker(location_values.latlng, tooltip=car_advert.location, popup=f'<img src="{ car_advert.get_first_image() }" width="50px" height="50px" alt="img">').add_to(map)
        # Getting HTML representation of the Map Object
    cars_map = map._repr_html_()

    context = {
            "car_adverts": car_adverts,
            "user_profile": user_profile,
            "cars_map": cars_map,
    }
    return render(request, "car_auctions/cars_observed.html", context)


@login_required(login_url="/users/accounts/login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def car_adverts_viewed(request):
    """
    Display a list of recently viewed car advertisements.
    Display an individual :model: 'car_auctions.CarAdvert'.

    **Context**

    ''recently_viewed''
        An instance of filtered :model: 'car_auctions.RecentlyViewed"

    **Template**

    :template: 'car_auctions/cars_browsed_history.html'
    """
    recently_viewed = RecentlyViewed.objects.filter(user=request.user).order_by(
        "-viewed_at"
    )[:100]
    context = {"recently_viewed": recently_viewed}
    return render(request, "car_auctions/cars_browsed_history.html", context)


@login_required(login_url="/users/accounts/login")
def car_advert_add(request):
    """
    Adding new car advert to the database. Displaying the list of added cars by the user.

    **Context**

    ''car_add_form''
        An instance of :form: 'car_auctions.CarAdvertAddForm'
    ''images_add_form''
        An instance of :filter: 'car_auctions.ImageForm'

    **Template**

    :template: 'car_auctions/car_add.html'
    """

    car_adverts = CarAdvert.objects.filter(owner=request.user)
    car_adverts = CarAdvertSearchFilter(request.GET, queryset=car_adverts)
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":
        car_advert_add_form = CarAdvertAddForm(request.POST)
        images_add_form = ImageForm(request.POST, request.FILES)
        if car_advert_add_form.is_valid() and images_add_form.is_valid():
            # Create a car instance
            car_advert_instance = car_advert_add_form.save(commit=False)
            car_advert_instance.owner = request.user
            car_advert_instance.save()

            # Creating car images as being related to car object.
            images = request.FILES.getlist("image")
            for car_image in images:
                CarImage.objects.create(car_advert=car_advert_instance, image=car_image)
            messages.add_message(request, messages.INFO, "Car added")
            # Form with no data after adding a car.
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            messages.add_message(request, messages.INFO, "Failed to add a car")
    else:
        car_advert_add_form = CarAdvertAddForm()
        images_add_form = ImageForm()

    context = {
        "car_adverts": car_adverts,
        "user_profile": user_profile,
        "car_advert_add_form": car_advert_add_form,
        "images_add_form": images_add_form,
    }
    return render(request, "car_auctions/car_add.html", context)

@login_required(login_url="/users/accounts/login")
def car_advert_data(request):
    """
    User's car adverts data

    **Context**

    **Template**

    :template: 'car_auctions/car_data.html'
    """

    user_profile = get_object_or_404(UserProfile, user=request.user)
    user_car_adverts = CarAdvert.objects.filter(owner=request.user)

    context = {
            'user_profile': user_profile,
            'user_car_adverts': user_car_adverts
    }
    return render(request, "car_auctions/car_data.html", context)


@login_required(login_url="/users/accounts/login")
def dashboard(request):
    """
    Display user-specific view of functionalities.
    Display a list of all car advertisements added by user in the form of filter to make available operation of filtering.
    Display a list of car advertisements that are observed by the user.
    Adding new car advert to the database.

    **Context**

    ''car_adverts''
        An instance of :model: 'car_auctions.CarAdvert'.
    ''car_add_form''
        An instance of :form: 'car_auctions.CarAdvertAddForm'
    ''images_add_form''
        An instance of :filter: 'car_auctions.ImageForm'
    ''user_profile''
        An instance of :model: 'users.UserProfile'


    **Template**

    :template: 'car_auctions/user_dashboard.html'
    """
    car_adverts = CarAdvert.objects.filter(owner=request.user)
    car_adverts = CarAdvertSearchFilter(request.GET, queryset=car_adverts)
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":
        car_advert_add_form = CarAdvertAddForm(request.POST)
        images_add_form = ImageForm(request.POST, request.FILES)
        if car_advert_add_form.is_valid() and images_add_form.is_valid():
            # Create a car instance
            car_advert_instance = car_advert_add_form.save(commit=False)
            car_advert_instance.owner = request.user
            car_advert_instance.save()

            # Creating car images as being related to car object.
            images = request.FILES.getlist("image")
            for car_image in images:
                CarImage.objects.create(car_advert=car_advert_instance, image=car_image)
            messages.add_message(request, messages.INFO, "Car added")
            # Form with no data after adding a car.
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            messages.add_message(request, messages.INFO, "Failed to add a car")
    else:
        car_advert_add_form = CarAdvertAddForm()
        images_add_form = ImageForm()

    context = {
        "car_adverts": car_adverts,
        "car_advert_add_form": car_advert_add_form,
        "images_add_form": images_add_form,
        "user_profile": user_profile,
    }
    return render(request, "car_auctions/user_dashboard.html", context)


@login_required(login_url="/users/accounts/login")
def car_advert_edit(request, pk):
    """
    Allows user to edit car details and images.

    **Context**

    ''car''
        An instance of :model: 'car_auctions.CarAdvert'.
    ''car_add_form''
        An instance of :form: 'car_auctions.CarAdvertAddForm'
    ''images_add_form''
        An instance of :filter: 'car_auctions.ImageForm'
    ''user_profile''
        An instance of :model: 'users.UserProfile'


    **Template**

    :template: 'car_auctions/user_dashboard.html'
    """
    car_advert = get_object_or_404(CarAdvert, pk=pk)
    car_image_default = CarImage.objects.filter(car_advert=car_advert).first()

    if request.method == "POST":
        car_advert_edit_form = CarAdvertAddForm(request.POST, instance=car_advert)
        images_edit_form = ImageForm(request.POST, request.FILES)
        if car_advert_edit_form.is_valid() and images_edit_form.is_valid():
            # Create a car instance.
            car_advert_instance = car_advert_edit_form.save(commit=False)
            car_advert_instance.owner = request.user
            car_advert_instance.save()

            # Deleting the default car image.
            images_empty = len(request.FILES.getlist("image"))
            # If there is a car image object and its image is default, and images are added through the form,
            # then the deletion of the default image occurs only when new images are being added through from.
            if (
                car_image_default is not None
                and car_image_default.image == "images/no_car_image.png"
                and images_empty != 0
            ):
                car_image_default.delete()

            # Create car images as being related to car object.
            images = request.FILES.getlist("image")

            for car_image in images:
                CarImage.objects.create(car_advert=car_advert_instance, image=car_image)
            messages.add_message(request, messages.INFO, "Car modified")
            # Form with no data after adding a car.
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            messages.add_message(request, messages.INFO, "Failed to modify a car")
    else:
        car_advert_edit_form = CarAdvertAddForm(instance=car_advert)
        images_add_form = ImageForm()

    context = {
        "car_advert": car_advert,
        "car_advert_edit_form": car_advert_edit_form,
        "images_add_form": images_add_form,
    }
    return render(request, "car_auctions/car_edit2.html", context)
