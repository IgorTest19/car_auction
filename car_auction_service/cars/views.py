from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Car, CarImage
from .forms import CarAddForm, ImageForm
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

    # if request.method == 'POST':
    #     print("-----2-----request.method == POST")
    #     print(request.method)
    #     print("------3--------data=request.POST")
    #     print(request.POST)
    #     car_add_form = CarAddForm(data=request.POST)
    #     print("------4--------car_add_form")
    #     print(car_add_form)
    #     if car_add_form.is_valid():
    #         print("-----5-------DID SAVE")
    #         car_add_form.save()
    #         car_add_form = CarAddForm()
    #         return render(request, 'cars/cars_main.html', {'cars': cars,
    #                                                        'car_add_form': car_add_form})
    # else:
    #     car_add_form = CarAddForm()

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

    return render(request, 'cars/cars_main.html', {'cars': cars, })
    # 'car_add_form':car_add_form})


def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    car_images = reversed(get_list_or_404(CarImage, car=car))
    return render(request, 'cars/car_detail.html', {'car': car,
                                                    'car_images': car_images})


@login_required
def car_delete(request, pk):
    car = get_object_or_404(Car, pk=pk)
    car.delete()
    return redirect('cars/user_dashboard.html')


def car_observe(request, pk):
    car = get_object_or_404(Car, pk=pk)
    user = User.objects.get(username=request.user.username)
    car.users_observing.add(user)
    car.save()

    return redirect('cars/user_dashboard.html')


# for single image
# @login_required
# def dashboard(request):
#     cars = Car.objects.all()
#     cars = CarSearchFilter(request.GET, queryset=cars)
#
#     # cars = CarSearchFilter(request.GET, queryset=cars) data=request.POST, request
#     if request.method == 'POST':
#         # car_add_form = CarAddForm(request.POST, request.FILES)
#         car_add_form = CarAddForm(request.POST)
#         image_form = ImageForm
#         print("----------request.FILES")
#         print(request.FILES)
#
#         # files = request.FILES.getlist('image')
#         if car_add_form.is_valid():
#             new_car = car_add_form.save(commit=False)
#             new_car.photo = request.FILES['photo'] # for single photo
#             new_car.owner = request.user
#             new_car.save()
#             car_add_form = CarAddForm() # clearing form
#             # for file in files:
#             #     Image.objects.create(car=new_car, image=file)
#             # messages.success(request, 'New car added')
#             print("-------request.car")
#             # print(request.body)
#             # return render(request, 'cars/car_add.html')W
#         else:
#             print(car_add_form.errors)
#     else:
#         car_add_form = CarAddForm()
#         # image_form = ImageForm
#
#     return render(request, 'cars/user_dashboard.html', {'cars': cars,
#                                                         'car_add_form': car_add_form})
#                                                         # 'image_form':image_form})


# Rozbić dashboard na osobno cad_add view i dashboard view
# for multiple images
# https://www.youtube.com/watch?v=HnxFAx1-jyU&ab_channel=StudyGyaan
# https://www.youtube.com/watch?v=cPcZFOZQNPA&ab_channel=JustSoondar

# spróbować tego:
# https://stackoverflow.com/questions/72591620/django-upload-multiple-images-per-post
# https://www.youtube.com/watch?v=psOQBoAmMhA&ab_channel=CodingEntrepreneurs
@login_required
def dashboard(request):
    # cars = Car.objects.all() # zrobić tutaj pobieranie obiektów po użytkwoniku
    cars = Car.objects.filter(owner=request.user) # tak działa wyświetlanie listy aut w dashboardzie tylko swoich dodanych aut :)
    cars = CarSearchFilter(request.GET, queryset=cars)
    car_add_form = CarAddForm()
    images_add_gorm = ImageForm()
    # cars = CarSearchFilter(request.GET, queryset=cars) data=request.POST, request
    if request.method == 'POST':
        # car_add_form = CarAddForm(request.POST, request.FILES)
        car_add_form = CarAddForm(request.POST)
        images_add_form = ImageForm(request.POST, request.FILES)
        images = request.FILES.getlist('image')

        # files = request.FILES.getlist('image')
        if car_add_form.is_valid() and images_add_form.is_valid():
            brand = car_add_form.cleaned_data['brand']
            model = car_add_form.cleaned_data['model']
            year = car_add_form.cleaned_data['year']
            # owner = request.user -> dodać to dalej
            print("==================== brand, year, model")
            print(brand, year, model)
            car_instance = Car.objects.create(brand=brand, model=model, year=year, owner=request.user)
            print("=================== car_instance")
            print(car_instance)
            for car_image in images:
                print("=============car image")
                print(car_image)
                CarImage.objects.create(car=car_instance, image=car_image)

            # new_car = car_add_form.save(commit=False)
            # new_car.owner = request.user
            # image_files= request.FILES.getlist('images')
            # for image in image_files:
            #     Image.objects.create(car = new_car, image=image)
            # new_car.save()
            # car_add_form = CarAddForm() # clearing form
            # print("-------request.car")
            # print(request.body)
            # return render(request, 'cars/car_add.html')W
        else:
            print(car_add_form.errors)
    else:
        car_add_form = CarAddForm()
        images_add_form = ImageForm()

    return render(request, 'cars/user_dashboard.html', {'cars': cars,
                                                        'car_add_form': car_add_form,
                                                        'images_add_form': images_add_form})
