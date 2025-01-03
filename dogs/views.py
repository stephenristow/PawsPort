from django.shortcuts import render, redirect
from django.contrib import messages
from .sql_queries import get_dog, get_dog_friend_list, get_dog_list, add_new_dog, get_breeds

def dog_profile_view(request, username, dog_name):
    try:
        curr_user = request.session['username']
        username = username
        dog = get_dog(username, dog_name)
        friends = get_dog_friend_list(username)
        return render(request, "dog_profile.html", {"curr_user": curr_user, "username": username, "dog": dog, "friends": friends})
    except KeyError as e:
        messages.error(request, f"You are not currently logged in. Please log in first or contact the administrator with this '{e}' in your message.")
        return redirect("login")


def dog_list(request):
    username = request.session['username']
    dogs = get_dog_list(username)
    return render(request, "dog_list", {"dogs": dogs})

def add_dog_view(request):
    try:
        username = request.session['username']
        breeds = get_breeds()
        if request.method == "POST":
            dog_name = request.POST.get("dog_name")
            bio = request.POST.get("bio")
            sex = request.POST.get("sex")
            age = request.POST.get("age")
            breed_name = request.POST.get("breed_name")
            add_new_dog(username, dog_name, bio, sex, age, breed_name)
            messages.success(request, f"Added new dog to your user profile. Welcome {dog_name}!")
            return redirect("dog_profile", username=username, dog_name=dog_name)
        return render(request, "add_dog.html", {"username": username, "breeds": breeds})
    except KeyError as e:
        messages.error(request, f"You are not currently logged in. Please log in first or contact the administrator with this '{e}' in your message.")
        return redirect("login")