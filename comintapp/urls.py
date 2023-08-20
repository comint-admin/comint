from django.urls import path

from .views import index

app_name = 'comintapp'
urlpatterns = [
    path('', index.handleRequest, name='index')
]