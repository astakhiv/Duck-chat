# DuckChat
## Distinctiveness and Complexity
This project is Django-based project. It is not any or like any of the other Web50 course projects. DuckChat contains JavaScript on the front-end and is moobile-responsive, because of Bootstrap 5 framework

## Files and folders
This project is made on `network` template, because of account system

As all of the other Django projects, DuckChat contains some base folders, such as: `project4/`, `network/`, `static/` and files `db.sqlite3` and `manage.py`

This project required `WebSocket` in it, so I needed such files: `asgi.py`, `routing.py`, `consumers.py`, `settings.py` and `chat.js`

### settings.py
Here I added `network`, `channels` and `daphne` apps to `INSTALLED_APPS`, so I could use them

To make requests be handeled by not by `wsgi.py`, but by `asgi.py`, I changed `WSGI_APPLICATION` to `ASGI_APPLICATION` 

Also, to set layers using `redis`, I added `CHANNEL_LAYERS` dict

### asgi.py
Usually, `application` in `asgi.py` deals only with http request, so here I had to use `ProtocolTypeRouter`

To deal with cross-site request forgery I used `AllowedHostsOriginValidator` objects to work with `websocket`

After than I user `URLRouter` to set routs, which should be used, when `websocket` connection is made

### routing.py
In this file I create routs, which will be used, when `websocket connection` is made

Also, when special url is called, I app uses ChatConsumer to deal with requests

### consumers.py
This is the biggest file

At the top of it I allow `DJANGO_ALLOW_ASYNC_UNSAFE` operations, such as database changes made asynchronously

After that I create class `ChatConsumer`, which inherits from `AsyncWebsocketConsumer` to allow getting and returning messages with `websocket` connection

Here are several methods:
1. `connect()` - to set connection on special layer and accept it
2. `disconnect()` - to discard connection on special layer
3. `receive()` - to get message, create instance of new message in special chat with sender and send it back with next method, so that JS script could show it to both users
4. `chat_message()` - to actually send message via WebSocket connection to the client

### chat.js
Here I set up a WedSocket connection via JS `WebSocket()` class and handle `onopen()`, `onmessage()` and `onclose()` functions

#

There are also some `http` requests in this app, so for it here are these files: `project4/urls.py`, `network/urls.py` and `views.py`

### project4/urls.py

Here I include `network/urls.py` to let it to handle http requests

### network/urls.py

For each veiw here is made a `path()` to handle each of them

### views.py

Here are some views to work:
1. `login_view()`, `logout_view()` and `register()` to deal with accounts and registration 
2. `get_user_chats(user)` is function to get all chats, where passed user is a participant. It exists, because almost on each page is a list of users chats, so I can call it for each view
3. `index()` this view is used to show the index page with list of chats, where user is in
4. `search()` this view is used to find all users, whose names contains given string and returns them and as index - chats
5. `chat(user)` this view is used to get all messages from chat, which is opened by user. If such chat doesn`t in the database, new chat is created
6. `darck_mode()` this view is used to turn ON/OFF the dark mode on the web site and redirects user to the index page

Each of these views requires `dark` propertie to send it to the client to set dark of light styles

### models.py

Here are 3 main models:
1. `User`, where is special field - `dark`, to track if user uses dark mode
2. `Chat` to split all messages between chats. Each chat has at least two participants
3. `Message` which is an object on message and has: `chat`(where it was sent), `sender`(User, who sent it) and `message`(the content of the message)

All of these models is registred in `admin.py`

Static files has 3 `.css` files and 1 `.js` file

1. `chat.js` was explained above
2. `dark.css` are styles for dark mode
3. `light.css` are styles for light mode
4. `styles.css` are styles for registration and login pages

## How to start project

For this you will need docker and redis-server
```
sudo apt-get install redis-server
sudo service redis-server start
sudo docker run -p 8000:8000 -d redis:5
```

You can download docker from [official Docker site](https://www.docker.com/products/docker-desktop/)

Also, you have to install all pythonpackages from `requirements.txt`

Afret that, run command 

```
python3 manage.py runserver
```

and you will see this project to `localhost:8000`

## Additional
While creating this project, I learned how to deal with WebSocket connection in JS and Django, work with layers and lots of other things

I hope that I will continue developing this project, despite school and comming exams

I still have lots of ideas to implement here, so thanks to Harvard University, David J. Malan and Brian Yu, who are main lectors of Web50 for all of job done by them to give this project life

I hope that this project will be great practice in future for me