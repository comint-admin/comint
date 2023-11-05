from django.urls import path

from .views import *

app_name = 'comintapp'
urlpatterns = [
    path('', index_views.IndexView.as_view(), name='index'),
    path('loans/', loan_views.loanView, name='loans'),
    path('fund_requests/', payment_views.fundRequests, name='fund_requests'),
    path('payments/', payment_views.payments, name='payments')
]