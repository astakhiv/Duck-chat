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
        user = User.objects.get(username=user)
        chats = []
        for i in Chat.objects.all():
            cur_partic = i.participants.all()
            if cur_partic.contains(user):
                receiver = cur_partic[0 if cur_partic[0] != user else 1]
                chats += [receiver.username]
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
    receiver = User.objects.get(username=user)
    sender = User.objects.get(username=request.user)
    chats = Chat.objects.all()
    chat = None

    for i in chats:
        if receiver in i.participants.all() and sender in i.participants.all():
            chat = i
            break

    messages = None

    if not chat:
        new_chat = Chat.objects.create()
        new_chat.participants.add(receiver)
        new_chat.participants.add(sender)
        new_chat.save()
    else:
        messages = Message.objects.filter(chat=chat)

    return render(request, "network/chat.html", {
        "chats": get_user_chats(request.user),
        "chat_with": user, 
        "user": request.user,
        "messages": reversed(messages) if messages else None
    })