
from django.urls import path, include 
from . import views

urlpatterns = [
    path('new/', views.register_vote),
    path('', views.join_vote),
    path('profile/', views.profile)
]