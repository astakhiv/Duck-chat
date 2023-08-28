import json

from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Chat, Message




def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def get_user_chats(user):
    # Defining chats to send to the template
        chats = []
        for i in Chat.objects.all():
            cur_partic = i.participants.all()
            if user in cur_partic:
                user = cur_partic[0 if cur_partic[0] != user else 1]
                chats += [user.username]
        return chats

def index(request):
    if request.user.is_authenticated:
        # Defining chats to send to the template
        chats = get_user_chats(request.user)

        return render(request, "network/index.html", {
            "chats": chats,
        })
    
    else:
        return HttpResponseRedirect(reverse("login"))


def search(request):
    # Method should work only when request method is POST
    if request.method == 'POST':
        #Get the username from request
        username = request.POST.get('username').lower()
        if username == "":
            return HttpResponseRedirect(reverse('index'))
        
        # Select all users with such input
        chats = []
        for user in User.objects.all():
            # User must not be able to type to him/her
            if user == User.objects.get(username=request.user):
                continue
            if user.username != request.user and username in user.username.lower():
                chats.append(user.username)

        return render(request, 'network/search.html', {
            "found_chats": chats,
            "chats": get_user_chats(request.user)
        })
    else:
        return HttpResponseRedirect(reverse('index'))


def chat(request, user):
    print(f"Receiver {user}")
    receiver = User.objects.filter(username=user)
    print(receiver)
    sender = User.objects.get(username=request.user)
    chat = Chat.objects.filter(participants__in=[
        User.objects.get(username=user),
        User.objects.get(username=request.user)
    ])[0]

    messages = Message.objects.filter(chat=chat)    

    return render(request, "network/chat.html", {
        "chats": get_user_chats(request.user),
        "chat_with": user, 
        "user": request.user,
        "messages": reversed(messages)
    })
