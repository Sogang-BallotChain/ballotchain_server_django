
from django.urls import path, include 
from . import views

urlpatterns = [
    path('register/', views.register_vote),
    path('', views.join_vote),
    path('profile/', views.profile),
    path('<vote_id>', views.info)
]