from django.urls import path
from .HomeWork_1 import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
]