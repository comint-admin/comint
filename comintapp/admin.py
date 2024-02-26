from django.contrib import admin
from .models import ComintUser, VerificationQuestion, UserProfile, LoanRequest, LineOfCredit, LOCNegotiationRequest, LOCConfirmation

# Existing Admin classes
class VerificationQuestionInline(admin.TabularInline):
    model = VerificationQuestion
    extra = 0

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class ComintUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')
    inlines = [UserProfileInline, VerificationQuestionInline]

# New Admin classes for Loan Features
class LoanRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'amount', 'term', 'interest_rate', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'description', 'user__email')

class LineOfCreditAdmin(admin.ModelAdmin):
    list_display = ('loan_request', 'negotiator')
    list_filter = ('loan_request__status',)
    search_fields = ('loan_request__name', 'negotiator__email')

class LOCNegotiationRequestAdmin(admin.ModelAdmin):
    list_display = ('line_of_credit', 'request_creator', 'amount', 'term', 'interest_rate', 'status', 'created_at','updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('line_of_credit__loan_request__name', 'request_creator__email')
    readonly_fields = ('updated_at',)  # Marking updated_at as read-only

class LOCConfirmationAdmin(admin.ModelAdmin):
    list_display = ('loc_negotiation_request', 'confirmed', 'confirmed_at')
    list_filter = ('confirmed',)
    search_fields = ('loc_negotiation_request__line_of_credit__loan_request__name',)

# Registering models with their admin classes
admin.site.register(ComintUser, ComintUserAdmin)
admin.site.register(LoanRequest, LoanRequestAdmin)
admin.site.register(LineOfCredit, LineOfCreditAdmin)
admin.site.register(LOCNegotiationRequest, LOCNegotiationRequestAdmin)
admin.site.register(LOCConfirmation, LOCConfirmationAdmin)
