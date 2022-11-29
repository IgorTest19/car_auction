from django.shortcuts import render

from .forms import UserRegistrationForm

# Create your views here.

def register(request):
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
            return render(request, 'cars/user_dashboard.html', {'new_user':new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'users/register.html', {'user_form':user_form})
    #TODO: add templates register_done and register
