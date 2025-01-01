from django.shortcuts import render, redirect
from django.contrib import messages
from .sql_queries import get_pending_received_requests, get_pending_sent_requests, accept_friend_request, reject_friend_request, cancel_friend_request, create_new_friend_request

def requests_view(request):
    try:
        username = request.session['username']
        raw_received_requests = get_pending_received_requests(username)
        raw_sent_requests = get_pending_sent_requests(username)

        received_requests = [req for req in raw_received_requests if req.get('username') is not None]
        sent_requests = [req for req in raw_sent_requests if req.get('friend_username') is not None]

        context = {
            'username':username, 
            'received_requests':received_requests, 
            'sent_requests':sent_requests,
            'has_received_requests': bool(received_requests),
            'has_sent_requests': bool(sent_requests)
        }
        return render(request, "requests.html", context)
    except KeyError as e:
        messages.error(request, f"You are not currently logged in. Please log in first or contact the administrator with this '{e}' in your message.")
        return redirect("login")

def send_request(request):
    username = request.session['username']
    friend_username = request.POST.get('friend_username')
    create_new_friend_request(username, friend_username)
    return redirect("user_profile", username=friend_username)

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
