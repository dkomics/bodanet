from django.urls import path
from . import views

urlpatterns = [
    path('ping/', views.ping, name='ping'),
    path('stands/', views.list_stands, name='list-stands'),
]