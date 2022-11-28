from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Car, Image
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

    return render(request, 'cars/cars_main.html', {'cars': cars,})
                                                   # 'car_add_form':car_add_form})


def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'cars/car_detail.html', {'car':car})

@login_required
def car_delete(request, pk):
    car = get_object_or_404(Car, pk=pk)
    car.delete()
    return redirect('cars/user_dashboard.html')

#for single image
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

# for multiple images
@login_required
def dashboard(request):
    cars = Car.objects.all()
    cars = CarSearchFilter(request.GET, queryset=cars)

    # cars = CarSearchFilter(request.GET, queryset=cars) data=request.POST, request
    if request.method == 'POST':
        # car_add_form = CarAddForm(request.POST, request.FILES)
        car_add_form = CarAddForm(request.POST)
        image_form = ImageForm
        print("----------request.FILES")
        print(request.FILES)

        # files = request.FILES.getlist('image')
        if car_add_form.is_valid():
            new_car = car_add_form.save(commit=False)
            new_car.images = request.FILES.getlist('images')
            new_car.owner = request.user
            new_car.save()
            car_add_form = CarAddForm() # clearing form
            # for file in files:
            #     Image.objects.create(car=new_car, image=file)
            # messages.success(request, 'New car added')
            print("-------request.car")
            # print(request.body)
            # return render(request, 'cars/car_add.html')W
        else:
            print(car_add_form.errors)
    else:
        car_add_form = CarAddForm()
        # image_form = ImageForm

    return render(request, 'cars/user_dashboard.html', {'cars': cars,
                                                        'car_add_form': car_add_form})
#                                                         # 'image_form':image_form})
