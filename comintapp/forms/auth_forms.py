from django import forms
from allauth.account.forms import SignupForm, LoginForm
from comintapp.models import ComintUser,VerificationQuestion, UserProfile
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
#from hcaptcha_field import hCaptchaField


class CoMintSignInForm(LoginForm):
    captcha = hCaptchaField()


class ComintSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name', required=False)
    verification_question_1 = forms.ChoiceField(choices=VerificationQuestion.VERIFICATION_QUESTIONS, label='Verification Question 1')
    verification_answer_1 = forms.CharField(max_length=255, label='Answer 1')
    verification_question_2 = forms.ChoiceField(choices=VerificationQuestion.VERIFICATION_QUESTIONS, label='Verification Question 2')
    verification_answer_2 = forms.CharField(max_length=255, label='Answer 2')
    verification_question_3 = forms.ChoiceField(choices=VerificationQuestion.VERIFICATION_QUESTIONS, label='Verification Question 3')
    verification_answer_3 = forms.CharField(max_length=255, label='Answer 3')

    
    tc = forms.BooleanField(required=True, label='I accept terms and conditions', label_suffix='')
    captcha = hCaptchaField()

    field_order = ['email', 'first_name', 'last_name', 'password1', 'password2', 'verification_question_1', 'verification_answer_1', 'verification_question_2', 'verification_answer_2', 'verification_question_3', 'verification_answer_3', 'tc', 'captcha']

    def clean_email(self):
        email = self.cleaned_data['email']
        if ComintUser.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists. Please login instead.")
        return email

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        for i in range(1, 4):
            question_field = f'verification_question_{i}'
            answer_field = f'verification_answer_{i}'
            VerificationQuestion.objects.create(
                user=user,
                question=self.cleaned_data[question_field],
                answer=self.cleaned_data[answer_field]
            )
        user.save()
        return user
    

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['dob', 'ssn', 'address_1', 'address_2', 'state', 'zip_code', 'consent_for_verification']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }