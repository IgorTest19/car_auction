from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import UserProfile
from .models import Car, CarImage
from .forms import CarAddForm, ImageForm
from .filters import CarSearchFilter
import folium

def cars_list(request):
    cars = Car.objects.all()
    cars = CarSearchFilter(request.GET, queryset=cars)
    return render(request, 'cars/cars_main.html', {'cars': cars, })


def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    car_images = reversed(get_list_or_404(CarImage, car=car))
    # adding map component
    # Creating Map Object
    cars_map = folium.Map(location=[50, 20], zoom_start=6)
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
    return redirect('cars/user_dashboard.html')


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
            car_instance = Car.objects.create(
                brand=brand, model=model, year=year, owner=request.user)
            for car_image in images:
                CarImage.objects.create(car=car_instance, image=car_image)
            messages.success(request, "Adding car was successful")
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
