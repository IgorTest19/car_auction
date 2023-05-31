from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import UserRegistrationForm, UserLoginForm, SetPasswordForm


def user_register(request):
    """
    Functionality allowing to register an user, creating a
    single instance of :model: 'auth.User'.

    **Context**

    ''user_form''
        An instance of :forms: 'users.UserRegistrationForm'


    **Template**

    :template: 'users/register.html'
    """
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            return render(request, "users/register_done.html", {"new_user": new_user})
    else:
        user_form = UserRegistrationForm()
    context = {"user_form": user_form}
    return render(request, "users/register.html", context)
    # TODO: add templates register_done and register


def user_login(request):
    """
    Functionality allowing user to log in.

    **Context**

    ''login_form''
        An instance of :forms: 'users.UserLoginForm'


    **Template**

    :template: 'users/login2.html'
    """
    # TODO ADD messages and crispy forms
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            cleaned_data = login_form.cleaned_data
            user = authenticate(
                username=cleaned_data["username"], password=cleaned_data["password"]
            )
            if user is not None:
                login(request, user)
                # return HttpResponse('Authentication was successful.')
                return redirect("car_auctions:cars_main")
            else:
                # return HttpResponse('Logging failed.')
                return redirect("users:login")
        else:
            # return HttpResponse('Wrong logging data.')
            return redirect("users:login")
    else:
        login_form = UserLoginForm()
    context = {"login_form": login_form}
    return render(request, "users/login2.html", context)


def user_logout(request):
    """
    Functionality allowing user to log out.

    """
    logout(request)
    return redirect("car_auctions:cars_main")


@login_required(login_url="/users/accounts/login")
def user_password_change(request):
    """
    Functionality allowing user to change it's password.

    **Context**

    ''change_password_form''
        An instance of :forms: 'users.SetPasswordForm'


    **Template**

    :template: 'user_password_change.html''
    """
    user = request.user
    if request.method == "POST":
        change_password_form = SetPasswordForm(user, request.POST)
        if change_password_form.is_valid():
            change_password_form.save()
            return redirect("users:login2.html")
        else:
            return HttpResponse("Wrong data.")
    change_password_form = SetPasswordForm(user)
    context = {"change_password_form": change_password_form}
    return render(request, "users/user_password_change.html", context)


def user_settings(request):
    """
    Functionality allowing user to log out.

    **Context**

    None


    **Template**

    :template: 'user_settings.html'
    """
    context = None
    return render(request, "users/user_settings.html", context)
