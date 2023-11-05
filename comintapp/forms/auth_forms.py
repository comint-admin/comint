from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
#from hcaptcha_field import hCaptchaField

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254, required=True)
    password = forms.CharField(label='Password', max_length=64, widget=forms.PasswordInput, required=True)

    class Meta:
        model = get_user_model()

class RegistrationForm(UserCreationForm):
    #hcaptcha = hCaptchaField()

    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name')