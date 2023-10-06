from django.contrib.auth.views import LoginView, LogoutView
from django.forms.forms import BaseForm
from django.http.response import HttpResponse
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from ..forms import auth_forms
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from verify_email.email_handler import send_verification_email

class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'comintapp/login.html'
    redirect_authenticated_user = True
    show_error_messages = True
    success_message ='Logged In Successfully.'
    def form_valid(self, form: BaseForm) -> HttpResponse:
          if not self.request.user.is_active:
                print("User: ", self.request.user, " not active")
          return super().form_valid(form)
    
    def get_success_url(self):
            return reverse_lazy('comintapp:payments')  
    

class RegisterView(SuccessMessageMixin, CreateView):
    model = get_user_model()
    template_name = 'comintapp/register.html'
    redirect_authenticated_user = True
    form_class = auth_forms.RegistrationForm
    success_message ='Account created successfully. Please verify using link in email.'

    def form_valid(self, form: BaseForm) -> HttpResponse:
        inactive_user = send_verification_email(self.request, form)
        print(inactive_user)
        
        return super().form_valid(form)

    def get_success_url(self):
            return reverse_lazy('comintapp:login')  