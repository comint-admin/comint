from django.urls import path

from .views import *

app_name = 'comintapp'
urlpatterns = [
    path('', index_views.IndexView.as_view(), name='index'),
    path('loans/', index_views.loanView, name='loans'),
    path('fund_requests/', index_views.fundRequests, name='fund_requests'),
    path('payments/', index_views.payments, name='payments'),
    path('tnc/', index_views.TncView.as_view(), name='tnc_page'),
    path('privacy/', index_views.PrivacyView.as_view(), name='privacy_page'),
    path('about/', index_views.AboutView.as_view(), name='about'),
    path('contact/', index_views.ContactView.as_view(), name='contact'),
    path('complete-profile/', auth_views.complete_profile, name='complete_profile'),
    path('verification-questions/', auth_views.verification_questions, name='verification_questions'),
    path('cashboard/', cashboard_views.CashboardView.as_view(), name='cashboard'),
    path('cashboard/lender', cashboard_views.LenderView.as_view(), name='lender_view'),
    path('cashboard/borrower', cashboard_views.BorrowerView.as_view(), name='borrower_view'),
    path('create_loan_request/', LoanRequestCreateView.as_view(), name='create_loan_request'),
    path('marketplace/', MarketplaceView.as_view(), name='marketplace'),
]
