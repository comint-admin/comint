from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from functools import wraps
from comintapp.models import UserProfile

def profile_verified_required(view_func):
    @wraps(view_func)
    @login_required  # Ensure the user is logged in
    def _wrapped_view(request, *args, **kwargs):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            if user_profile.is_verified and user_profile.is_complete:
                return view_func(request, *args, **kwargs)
            elif not user_profile.is_complete:
                # Inform the user that they need to complete their profile
                messages.warning(request, "You must complete your profile before accessing that feature.")
                return redirect('comintapp:complete_profile')  # Redirect to profile completion page
            else:
                # Message updated to use messages.info for consistency
                messages.warning(request, "Your profile is currently undergoing verification. Please wait till it is verified to access full functionality of the site.")
                return redirect('comintapp:cashboard')  # Or another page as needed
        except UserProfile.DoesNotExist:
            messages.warning(request, "You need to complete your profile first.")
            return redirect('comintapp:complete_profile')
    return _wrapped_view
