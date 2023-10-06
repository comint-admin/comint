from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254, required=True)
    password = forms.CharField(label='Password', max_length=64, widget=forms.PasswordInput, required=True)
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Get the 'request' argument and remove it from kwargs
        super().__init__(*args, **kwargs)  # Call the parent class's __init__ method
    

    class Meta:
        model = get_user_model()

class RegistrationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name')