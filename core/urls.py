from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("user_profile/<str:username>/", views.user_profile_view, name="user_profile"),
]