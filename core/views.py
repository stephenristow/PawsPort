from django.shortcuts import render, redirect
from django.contrib import messages
from users.sql_queries import get_user, does_user_exist, create_user, does_email_exist
from friendships.sql_queries import get_pending_received_requests, get_pending_sent_requests, accept_friend_request, reject_friend_request, cancel_friend_request
from dogs.sql_queries import get_dog, get_dogs, get_dog_friend_list, get_dog_list, add_new_dog
from django.http import HttpResponse

def index_view(request):
    username = request.session['username']
    dogs = get_dogs(username)
    friends = get_dog_friend_list(username)

    return render(request, "index.html", {"username": username, "dogs": dogs, "friends": friends})