from django.contrib import admin
from comintapp.models import ComintUser, VerificationQuestion

# Inline admin for Verification Questions
class VerificationQuestionInline(admin.TabularInline):
    model = VerificationQuestion
    fields = ('question', 'answer')  # Specify the fields to display
    extra = 0  # Removes extra empty fields

# Updated ComintUser admin to include inline for Verification Questions
class ComintUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')
    inlines = [VerificationQuestionInline]

admin.site.register(ComintUser, ComintUserAdmin)
