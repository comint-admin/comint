from django.urls import path

from .views import *

app_name = 'comintapp'
urlpatterns = [
    path('', index_views.handleRequest, name='index'),
    path('register/', auth_views.register, name='register'),
    path('login/', auth_views.user_login , name='login'),
    path('logout/', auth_views.user_logout, name='logout'),
    path('loans/', loan_views.loanView, name='loans'),
    path('fund_requests/', payment_views.fundRequests, name='fund_requests'),
    path('payments/', payment_views.payments, name='payments')
]