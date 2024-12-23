from django.shortcuts import render, redirect
from django.contrib import messages
from .sql_queries import get_dog, get_dog_friend_list, get_dog_list, add_new_dog

def dog_profile_view(request, username, dog_name):
    dog = get_dog(username, dog_name)
    friends = get_dog_friend_list(username)
    return render(request, "dog_profile", {"dog": dog, "friends": friends})

def dog_list(request):
    username = request.session['username']
    dogs = get_dog_list(username)
    return render(request, "dog_list", {"dogs": dogs})

def add_dog_view(request):
    if request.method == "POST":
        username = request.session['username']
        dog_name = request.POST.get("dog_name")
        bio = request.POST.get("bio")
        sex = request.POST.get("sex")
        age = request.POST.get("age")
        add_new_dog(username, dog_name, bio, sex, age)
        messages.success(f"Added new dog to your user. Welcome {dog_name}!")
        return redirect("dog_profile_view", username=username, dog_name=dog_name)
    return render(request, "add_dog")