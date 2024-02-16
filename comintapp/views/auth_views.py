# In your views.py
from django.shortcuts import render, redirect
from comintapp.forms import UserProfileForm, VerificationQuestionsForm
from comintapp.models import UserProfile, VerificationQuestion
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def verification_questions(request):
    if not request.user.is_authenticated:
        return redirect('account_login')

    if request.method == 'POST':
        form = VerificationQuestionsForm(request.POST)
        if form.is_valid():
            user = request.user
            VerificationQuestion.objects.filter(user=user).delete()  # Remove existing questions for this user

            # Create new verification questions
            for i in range(1, 4):
                question_field = f'verification_question_{i}'
                answer_field = f'verification_answer_{i}'
                VerificationQuestion.objects.create(
                    user=user,
                    question=form.cleaned_data[question_field],
                    answer=form.cleaned_data[answer_field]
                )

            # Redirect to profile completion
            return redirect('comintapp:complete_profile')
    else:
        form = VerificationQuestionsForm()

    return render(request, 'comintapp/verification_questions.html', {'form': form})

@login_required
def complete_profile(request):
    user = request.user
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
            profile = form.save(commit=False)
            profile.is_complete = True
            profile.save()
            messages.success(request, "Profile Status - In Progress! Our team is currently reviewing your profile. You will be notified of any updates via email.")
            return redirect('comintapp:cashboard')  
    else:
        if profile and profile.is_complete:
            return redirect('comintapp:cashboard')
        form = UserProfileForm(instance=profile) if profile else UserProfileForm()

    return render(request, 'comintapp/complete_profile.html', {'form': form})
