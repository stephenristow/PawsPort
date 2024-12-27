from django.shortcuts import render, redirect
from django.contrib import messages
from .sql_queries import get_user, does_user_exist, create_user, does_email_exist
from django.http import HttpResponse


def login_view(request):
    if request.POST.get("username") and request.POST.get("password"):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = get_user(username, password)
        if user:
            request.session['username'] = user
            return redirect('index')
        else:
            valid_username = does_user_exist(username)
            if not valid_username:
                messages.error(request, "That username does not exist. Please try again.")
                return redirect("login")

    return render(request, "login.html")

def logout_view(request):
    request.session.flush()
    messages.success(request, "You have been logged out.")
    return redirect("login")

def signup_view(request):
    if request.POST.get("username") and request.POST.get("password") and request.POST.get("email"):
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        if does_user_exist(username):
            messages.error(request, "That username already exists. Please pick another and try again.")
            return redirect("login")
        elif does_email_exist(email):
            messages.error(request, "That email is already being used by a user. Please login with the associated username or use another email.")
            return redirect("login")
        else:
            create_user(username, password, email)
            messages.success(request, f"User successfully created. Please log in with you details now!")
            return redirect("login")

    return render(request, "signup.html")