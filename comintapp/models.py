from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from allauth.account.signals import user_signed_up, email_confirmed
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import re

class CustomComintUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class ComintUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), blank=False, unique=True)
    first_name = models.CharField(_('first name'), max_length=40, blank=True, null=True, unique=False)
    last_name = models.CharField(_('last name'), max_length=40, blank=True, null=True, unique=False)
    display_name = models.CharField(_('display name'), max_length=20, blank=True, null=True, unique=False)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    
    objects = CustomComintUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'auth_user'
        abstract = False

    @property
    def name(self):
        if self.first_name:
            return self.first_name
        elif self.display_name:
            return self.display_name
        return 'User'

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def guess_display_name(self):
        """Set a display name, if one isn't already set."""
        if self.display_name:
            return

        if self.first_name and self.last_name:
            dn = "%s %s" % (self.first_name, self.last_name[0])  # like "Andrew E"
        elif self.first_name:
            dn = self.first_name
        else:
            dn = 'User'
        self.display_name = dn.strip()

    def __str__(self):
        return self.email

    def natural_key(self):
        return (self.email,)


@receiver(email_confirmed)
def update_user_profile(sender, request, email_address, **kwargs):
    """
    Create a user profile and update the is_verified field when the email is confirmed.
    """
    # Get the user based on the email address
    user = email_address.user

    # Check if the user already has a profile, create one if not
    UserProfile.objects.get_or_create(user=user)

    # Update the is_verified field in the user's profile
    user.profile.save()

class VerificationQuestion(models.Model):
    VERIFICATION_QUESTIONS = [
        ('childhood_nickname', 'What was your childhood nickname?'),
        ('favorite_childhood_friend', 'What is the name of your favorite childhood friend?'),
        ('parents_meet_city', 'In what city or town did your mother and father meet?'),
        ('favorite_team', 'What is your favorite team?'),
        ('dream_job_child', 'What was your dream job as a child?'),
        ('first_car_make_model', 'What was the make and model of your first car?'),
        ('hospital_born', 'What was the name of the hospital where you were born?'),
        ('childhood_sports_hero', 'Who is your childhood sports hero?'),
        ('mothers_maiden_name', 'What was your mother’s maiden name?'),
    ]

    user = models.ForeignKey(ComintUser, on_delete=models.CASCADE)
    question = models.CharField(max_length=255, choices=VERIFICATION_QUESTIONS)
    answer = models.CharField(max_length=255)

    def __str__(self):
        return self.get_question_display()

def validate_ssn(value):
    """
    Validates that the input is a valid SSN.
    Assumes the format to be "XXX-XX-XXXX" where X is a digit.
    """
    if not re.match(r'^\d{3}-\d{2}-\d{4}$', value):
        raise ValidationError(
            _('%(value)s is not a valid SSN'),
            params={'value': value},
        )

class UserProfile(models.Model):
    """Profile data about a user."""

    user = models.OneToOneField(ComintUser, primary_key=True, verbose_name='user', related_name='profile',
                                on_delete=models.CASCADE)

    avatar_url = models.CharField(max_length=256, blank=True, null=True)

    dob = models.DateField(verbose_name="Date of Birth", blank=True, null=True)
    ssn = models.CharField(
        verbose_name="SSN (optional)",
        max_length=11,
        validators=[validate_ssn],
        help_text="Social Security Number in the format XXX-XX-XXXX",
        blank=True,  
        null=True,
    )

    address_1 = models.CharField(max_length=255, verbose_name="Address 1")
    address_2 = models.CharField(max_length=255, verbose_name="Address 2", blank=True, null=True)
    state = models.CharField(max_length=100, verbose_name="State")
    zip_code = models.CharField(max_length=10, verbose_name="Zip Code")
    consent_for_verification = models.BooleanField(default=False, verbose_name="Consent for Identity Verification")
    is_verified = models.BooleanField(default=False, verbose_name="Is Verified")
    is_complete = models.BooleanField(default=False, verbose_name="Profile Completed")

    def __str__(self):
        return str(self.user.email)

    class Meta():
        db_table = 'user_profile'
    

@receiver(user_signed_up)
def set_initial_user_names(request, user, sociallogin=None, **kwargs):
    """
    When a social account is created successfully and this signal is received,
    django-allauth passes in the sociallogin param, giving access to metadata on the remote account, e.g.:
 
    sociallogin.account.provider  # e.g. 'twitter' 
    sociallogin.account.get_avatar_url()
    sociallogin.account.get_profile_url()
    sociallogin.account.extra_data['screen_name']
 
    See the socialaccount_socialaccount table for more in the 'extra_data' field.

    From http://birdhouse.org/blog/2013/12/03/django-allauth-retrieve-firstlast-names-from-fb-twitter-google/comment-page-1/
    """

    # preferred_avatar_size_pixels = 256

    # picture_url = "http://www.gravatar.com/avatar/{0}?s={1}".format(
    #     hashlib.md5(user.email.encode('UTF-8')).hexdigest(),
    #     preferred_avatar_size_pixels
    # )
    if sociallogin:
        # print(sociallogin.account.extra_data)
        # Extract first / last names from social nets and store on User record
        if sociallogin.account.provider == 'google':
            # print(sociallogin.account.extra_data)
            user.first_name = sociallogin.account.extra_data['given_name']
            if sociallogin.account.extra_data.get('family_name'):
                user.last_name = sociallogin.account.extra_data['family_name']
            else:
                user.last_name = ""
            # verified = sociallogin.account.extra_data['verified_email']
            # picture_url = sociallogin.account.extra_data['picture']

    user.guess_display_name()
    user.save()

class LoanRequest(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('EXPIRING', 'Expiring'),
        ('EXPIRED', 'Expired'),
        ('FUNDED', 'Funded'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(ComintUser, on_delete=models.CASCADE, related_name='loan_requests')
    term = models.IntegerField(help_text='Term in months')
    interest_rate = models.DecimalField(max_digits=5, decimal_places=1, help_text='Interest rate as a percentage')
    amount = models.DecimalField(max_digits=6, decimal_places=2, help_text='Loan amount in USD')
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OPEN')

    def __str__(self):
        return f'{self.name} - {self.user if self.user_id else ""}'


    def clean(self):
        if self.amount is not None and self.amount > 5000:
            raise ValidationError({'amount': 'Loan amount cannot exceed 5000 USD'})

class LineOfCredit(models.Model):
    loan_request = models.ForeignKey(LoanRequest, on_delete=models.CASCADE, related_name='lines_of_credit')
    negotiator = models.ForeignKey(ComintUser, on_delete=models.CASCADE, related_name='negotiated_loc')

    def __str__(self):
        return f'{self.loan_request} - {self.negotiator}'
    
    def save(self, *args, **kwargs):
        if self.negotiator == self.loan_request.user:
            raise ValidationError('A user cannot add a line of credit to their own loan')
        super().save(*args, **kwargs)


class LOCNegotiationRequest(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('COUNTERED', 'Countered'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
        ('CANCELLED', 'Cancelled'),
    ]

    line_of_credit = models.ForeignKey(LineOfCredit, on_delete=models.CASCADE, related_name='negotiations')
    request_creator = models.ForeignKey(ComintUser, on_delete=models.CASCADE, related_name='loc_negotiations')
    term = models.IntegerField(help_text='Term in months')
    interest_rate = models.DecimalField(max_digits=5, decimal_places=1, help_text='Interest rate as a percentage')
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text='Loan amount in USD')
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OPEN')

    def __str__(self):
        return f'Negotiation for {self.line_of_credit} by {self.request_creator}'

class LOCConfirmation(models.Model):
    loc_negotiation_request = models.OneToOneField(LOCNegotiationRequest, on_delete=models.CASCADE, related_name='confirmation')
    confirmed = models.BooleanField(default=False)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Confirmation for {self.loc_negotiation_request}'
