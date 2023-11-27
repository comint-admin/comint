from django import forms
from allauth.account.forms import SignupForm, LoginForm, ResetPasswordForm
from comintapp.models import ComintUser,VerificationQuestion, UserProfile
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.functional import lazy
from django.utils.translation import gettext as _
from hcaptcha_field import hCaptchaField


class CoMintSignInForm(LoginForm):
    captcha = hCaptchaField()


class ComintSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name', required=True)
    last_name = forms.CharField(max_length=30, label='Last Name', required=False)
    verification_question_1 = forms.ChoiceField(choices=VerificationQuestion.VERIFICATION_QUESTIONS, label='Verification Question 1')
    verification_answer_1 = forms.CharField(max_length=255, label='Answer 1', required=True)
    verification_question_2 = forms.ChoiceField(choices=VerificationQuestion.VERIFICATION_QUESTIONS, label='Verification Question 2')
    verification_answer_2 = forms.CharField(max_length=255, label='Answer 2', required=True)
    verification_question_3 = forms.ChoiceField(choices=VerificationQuestion.VERIFICATION_QUESTIONS, label='Verification Question 3')
    verification_answer_3 = forms.CharField(max_length=255, label='Answer 3', required=True)


    tc = forms.BooleanField(
        required=True,
        label = lazy(lambda: mark_safe(_(
            'I accept <a href="%s" target="_blank">Terms and Conditions</a>' % reverse('comintapp:tnc_page')
        ))),
        label_suffix=''
    )
    captcha = hCaptchaField()

    field_order = ['email', 'first_name', 'last_name', 'password1', 'password2', 'verification_question_1', 'verification_answer_1', 'verification_question_2', 'verification_answer_2', 'verification_question_3', 'verification_answer_3', 'tc', 'captcha']

    def clean_email(self):
        email = self.cleaned_data['email']
        if ComintUser.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists. Please login instead.")
        return email
    
    def clean(self):
        cleaned_data = super().clean()

        questions = [
            cleaned_data.get("verification_question_1"),
            cleaned_data.get("verification_question_2"),
            cleaned_data.get("verification_question_3")
        ]

        if len(set(questions)) != len(questions):
            raise forms.ValidationError("Please select different verification questions.")

        return cleaned_data
    
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

        def __init__(self, *args, **kwargs):
            super(UserProfileForm, self).__init__(*args, **kwargs)
            
            # List of fields that should be required
            required_fields = ['dob', 'address_1', 'state', 'zip_code', 'consent_for_verification']

            # Set required attribute for the fields in the list
            for field_name in required_fields:
                self.fields[field_name].required = True



class ComintResetPasswordForm(ResetPasswordForm):
    def clean_email(self):
        email = self.cleaned_data["email"]
        UserModel = get_user_model()
        if not UserModel.objects.filter(email__iexact=email, is_active=True).exists():
            raise ValidationError("No user registered with this email address.")
        return email

    def save(self, request, **kwargs):
        # Fetch the users before calling the super save method
        UserModel = get_user_model()
        self.users = UserModel.objects.filter(email__iexact=self.cleaned_data["email"], is_active=True)
        # Call the super method with the request and kwargs
        super().save(request, **kwargs)