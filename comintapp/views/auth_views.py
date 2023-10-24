from django.contrib.auth.views import LoginView, LogoutView
from django.forms.forms import BaseForm
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from ..forms import auth_forms
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'comintapp/login.html'
    redirect_authenticated_user = True
    show_error_messages = True
    success_message ='Logged In Successfully.'
    
    
    def get_success_url(self):
            return reverse_lazy('comintapp:payments')  
    

class RegisterView(SuccessMessageMixin, CreateView):
    model = get_user_model()
    template_name = 'comintapp/register.html'
    redirect_authenticated_user = True
    form_class = auth_forms.ComintSignupForm
    success_message ='Account created successfully. Please verify using link in email.'


    def get_success_url(self):
            return reverse_lazy('comintapp:login')  
    
    def form_invalid(self, form):
        if 'email' in form.errors and 'A user with this email already exists.' in form.errors['email']:
            messages.error(self.request, "A user with this email already exists. Please login instead.")
            return redirect('comintapp:account_login')
        return super().form_invalid(form)