from django.urls import path

from .views import *

app_name = 'comintapp'
urlpatterns = [
    path('', index_views.handleRequest, name='index'),
    path('logout/', LogoutView.as_view(next_page='comintapp:index'), name='logout'),
    path('loans/', loan_views.loanView, name='loans'),
    path('fund_requests/', payment_views.fundRequests, name='fund_requests'),
    path('payments/', payment_views.payments, name='payments')
]