from django.urls import path
from . import views

urlpatterns = [
    path("requests/", views.requests_view, name="requests_view"),
    path("accept_request/", views.accept_request, name="accept_request"),
    path("reject_request/", views.reject_request, name="reject_request"),
    path("cancel_request/", views.cancel_request, name="cancel_request"),
]