from django.urls import path
from . import views

urlpatterns = [
    path('fare/', views.get_fare, name='get-fare'),
]
