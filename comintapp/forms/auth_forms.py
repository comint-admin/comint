from django import forms
from allauth.account.forms import SignupForm
from comintapp.models import ComintUser
from django.core.exceptions import ValidationError
from django.shortcuts import redirect

class ComintSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name', required=False)

    def clean_email(self):
        email = self.cleaned_data['email']
        if ComintUser.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists. Please login instead.")
        return email

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user
