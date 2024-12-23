from django.urls import path
from . import views

urlpatterns = [
    path("dog_profile/", views.dog_profile_view, name="dog_profile"),
    path("dog_list/", views.dog_list, name="dog_list"),
    path("add_dog/", views.add_dog_view, name="add_dog"),
]