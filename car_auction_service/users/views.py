from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserLoginForm, SetPasswordForm
from django.http import HttpResponse


def user_register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'users/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'users/register.html', {'user_form': user_form})
    # TODO: add templates register_done and register


def user_login(request):
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
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


def user_logout(request):
    logout(request)
    return redirect('cars:cars_main')


@login_required(login_url='/users/accounts/login')
def user_password_change(request):
    user = request.user
    if request.method == "POST":
        change_password_form = SetPasswordForm(user, request.POST)
        if change_password_form.is_valid():
            change_password_form.save()
            return redirect('users:login2.html')
        else:
            return HttpResponse('Wrong data.')
    change_password_form = SetPasswordForm(user)
    return render(request, 'users/user_password_change.html', {'change_password_form': change_password_form})


def user_settings(request):
    content = None
    return render(request, 'users/user_settings.html', {'content': content})
