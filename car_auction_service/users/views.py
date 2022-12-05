from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm, UserLoginForm
from django.http import HttpResponse
# Create your views here.

def user_register(request):
    print('----if request.method == "POST"')
    print(request.method)
    if request.method == "POST":
        print("------request.POST")
        print(request.POST)
        user_form = UserRegistrationForm(request.POST)
        print('----------user_form')
        print(user_form)
        if user_form.is_valid():
            print('-----user_form.is_valid()')
            print(user_form.is_valid())
            new_user = user_form.save(commit=False)
            print("-------new_user")
            print(new_user)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'users/register_done.html', {'new_user':new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'users/register.html', {'user_form':user_form})
    #TODO: add templates register_done and register

def user_login(request):
    print("===================DONE0")
    # checking if request method is POST
    print(UserLoginForm())
    if request.method == "POST":
        print("===================DONE1")
        # filling login form with data from POST method from request
        login_form = UserLoginForm(request.POST)
        print("===================DONE2")
        # checking if login form data is valid, no errors
        if login_form.is_valid():
            cleaned_data = login_form.cleaned_data
            user = authenticate(username=cleaned_data['username'],
                                password=cleaned_data['password'])
            if user is not None:
                login(request, user)
                return HttpResponse('Authentication was successful.')
            else:
                return HttpResponse('Logging failed.')
        else:
            return HttpResponse('Wrong logging data.')
    else:
        login_form = UserLoginForm()
    return render(request, 'users/login2.html', {'login_form': login_form})