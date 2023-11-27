# In middleware.py or a similar file
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from comintapp.models import UserProfile

class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                profile_exists = True
            except UserProfile.DoesNotExist:
                profile_exists = False

            if profile_exists:
                if not profile.is_verified:
                     # If the profile exists but is not verified
                    messages.info(request, "Your profile is currently undergoing verification, please wait till it is verified to access full functionality of the site.")
                # Redirect to index in both cases if the current path is not index
            else:
                # If the profile does not exist
                if not request.session.get('profile_checked', False):
                    # If they have not been redirected once after login
                    request.session['profile_checked'] = True
                    return redirect('comintapp:complete_profile')
                else:
                    # If they have already been redirected once
                    messages.info(request, "Your profile is incomplete. Please complete it to access all features.")

        return self.get_response(request)
