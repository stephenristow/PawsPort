from django.shortcuts import render, redirect
from django.contrib import messages
from .sql_queries import get_pending_received_requests, get_pending_sent_requests, accept_friend_request, reject_friend_request, cancel_friend_request, create_new_friend_request

def requests_view(request):
    username = request.session['username']
    received_requests = get_pending_received_requests(username)
    sent_requests = get_pending_sent_requests(username)
    return render(request, "requests.html", {'username':username, 'received_requests':received_requests, 'sent_requests':sent_requests})

def send_request(request):
    username = request.session['username']
    friend_username = request.POST.get('friend_username')
    create_new_friend_request(username, friend_username)
    return redirect("user_profile")

def accept_request(request):
    friend_username = request.POST.get("friend_username")
    username = request.session['username']
    accept_friend_request(username, friend_username)

    return redirect("requests_view")

def reject_request(request):
    username = request.session['username']
    friend_username = request.POST.get("friend_username")
    reject_friend_request(username, friend_username)
    return redirect("requests_view")

def cancel_request(request):
    username = request.session['username']
    friend_username = request.POST.get("friend_username")
    cancel_friend_request(username, friend_username)
    return redirect("requests_view")
