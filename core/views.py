from django.shortcuts import render, redirect
from django.contrib import messages
from users.sql_queries import get_user, does_user_exist, create_user, does_email_exist
from friendships.sql_queries import get_pending_received_requests, get_pending_sent_requests, accept_friend_request, reject_friend_request, cancel_friend_request, is_friend
from dogs.sql_queries import get_dog, get_dogs, get_dog_friend_list, get_dog_list, add_new_dog
from django.http import HttpResponse

def index_view(request):
    try:
        username = request.session['username']
        dogs = get_dogs(username)
        friends = get_dog_friend_list(username)

        return render(request, "index.html", {"username": username, "dogs": dogs, "friends": friends})
    except KeyError as e:
        messages.error(request, f"You are not currently logged in. Please log in first or contact the administrator with this '{e}' in your message.")
        return redirect("login")

def user_profile_view(request, username):
    try:
        curr_user = request.session['username']
        if not curr_user:
                messages.error(request, "You are not currently logged in. Please log in first.")
                return redirect("login")
        dogs = get_dogs(username)
        friends = get_dog_friend_list(username)
        is_self = curr_user == username
        if is_self:
            is_friend_already = True
        else:
            is_friend_already = is_friend(curr_user, username)

        return render(request, "user_profile.html", {"curr_user": curr_user, "username": username, "dogs": dogs, "friends": friends, "is_self": is_self, "is_friend_already": is_friend_already})
    except KeyError as e:
        messages.error(request, f"You are not currently logged in. Please log in first or contact the administrator with this '{e}' in your message.")
        return redirect("login")