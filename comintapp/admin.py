from django.contrib import admin
from comintapp.models import ComintUser, VerificationQuestion, UserProfile

# Inline admin for Verification Questions
class VerificationQuestionInline(admin.TabularInline):
    model = VerificationQuestion
    fields = ('question', 'answer')  # Specify the fields to display
    extra = 0  # Removes extra empty fields

# Inline admin for User Profile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False  # Optional: set to False if you don't want to allow deleting profiles from user admin
    verbose_name_plural = 'UserProfile'  # Optional: sets the plural name for user profile section

# Updated ComintUser admin to include inlines for Verification Questions and User Profile
class ComintUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')
    inlines = [UserProfileInline, VerificationQuestionInline]

admin.site.register(ComintUser, ComintUserAdmin)
