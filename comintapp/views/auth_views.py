# In your views.py
from django.shortcuts import render, redirect
from comintapp.forms import UserProfileForm
from comintapp.models import UserProfile

def complete_profile(request):
    user = request.user
    profile = None
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        if not profile:
            # Create a new profile only if it does not exist and the form is being submitted
            profile = UserProfile(user=user)
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('comintapp:index')  
    else:
        form = UserProfileForm(instance=profile) if profile else UserProfileForm()

    return render(request, 'comintapp/complete_profile.html', {'form': form})
