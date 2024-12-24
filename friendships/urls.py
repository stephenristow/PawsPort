from django.urls import path
from . import views

urlpatterns = [
    path("requests/", views.requests_view, name="requests_view"),
    path("send_request/", views.send_request, name="send_request"),
    path("accept_request/", views.accept_request, name="accept_request"),
    path("reject_request/", views.reject_request, name="reject_request"),
    path("cancel_request/", views.cancel_request, name="cancel_request"),
]