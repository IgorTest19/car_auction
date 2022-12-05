from django.contrib.auth.models import User
from django import forms

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords are not the same!')
        return cd['password2']


#change for allauth !!!!!!!
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# class UserLoginForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('username', 'password')
