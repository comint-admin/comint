from django.urls import path

from .views import *

app_name = 'comintapp'
urlpatterns = [
    path('', index_views.IndexView.as_view(), name='index'),
    path('loans/', loan_views.loanView, name='loans'),
    path('fund_requests/', payment_views.fundRequests, name='fund_requests'),
    path('payments/', payment_views.payments, name='payments'),
    path('tnc/', index_views.TncView.as_view(), name='tnc_page'),
    path('privacy/', index_views.PrivacyView.as_view(), name='privacy_page'),
    path('about/', about_views.AboutView.as_view(), name='about'),
    path('contact/', contact_views.ContactView.as_view(), name='contact'),
]
