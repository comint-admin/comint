# In middleware.py or a similar file
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from comintapp.models import UserProfile, VerificationQuestion

class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Exclude certain paths to avoid redirect loops
        if request.path in [reverse('account_login'), reverse('account_logout'), reverse('account_signup'), reverse('account_email_verification_sent')]:
            return self.get_response(request)
        
        if request.user.is_authenticated:
            questions_answered = VerificationQuestion.objects.filter(user=request.user).count() == 3
            profile_exists = UserProfile.objects.filter(user=request.user).exists()

            # Check if verification questions have been answered
            # questions_answered = request.session.get('verification_questions_answered', False)

            # Redirect to verification questions page if not answered
            if not questions_answered and request.path != reverse('comintapp:verification_questions'):
                messages.info(request, "You must complete the security questions to continue!")
                return redirect('comintapp:verification_questions')
            
            if profile_exists:
                profile = UserProfile.objects.get(user=request.user)
                if not profile.is_verified:
                     # If the profile exists but is not verified
                    messages.info(request, "Your profile is currently undergoing verification, please wait till it is verified to access full functionality of the site.")
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
