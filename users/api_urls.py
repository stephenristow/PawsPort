from django.urls import path
from .api_views import MeView, PublicProfileView

urlpatterns = [
    path("users/me", MeView.as_view(), name="users-me"),
    path("users/@<slug:username>", PublicProfileView.as_view(), name="users-public"),
]
