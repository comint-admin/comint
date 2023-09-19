# ------------------------------------------------------------------------------------------
# User authentication views
# ------------------------------------------------------------------------------------------
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from ..forms import auth_forms

def user_login(request):
    if request.method == 'POST':
        form = auth_forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                next_url = request.GET.get('next', 'handleRequest')  # Redirect to next URL or default to 'search'
                return redirect(next_url)
            else:
                messages.error(request, "Invalid Email or password.")
        else:
            pass
            # logger.warning("Invalid login form submission by %s", request.META.get('REMOTE_ADDR'))
    else:
        form = auth_forms.LoginForm()
    return render(request, 'comintapp/login.html', {'form': form})

def register(request):
    if request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = auth_forms.RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully.")
            return redirect('login')
        else:
            pass
            # logger.warning("Invalid registration form submission by %s", request.META.get('REMOTE_ADDR'))
    else:
        form = auth_forms.RegistrationForm()
    return render(request, 'comintapp/register.html', {'form': form, 'errors': form.errors, 'messages': messages.get_messages(request)})


@login_required
def user_logout(request):
    logout(request)
    return redirect('handleRequest')