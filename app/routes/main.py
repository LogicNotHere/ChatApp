from email.message import Message

from flask import jsonify, render_template, request, redirect, url_for, session, make_response
from pyexpat.errors import messages

from datetime import datetime, timezone, timedelta
from ..models.room import Room

from ..models.user import User
from ..redis import update_online_status, r
import os, json

from ..db import jwt, client  # вынести куда то
from functools import wraps  # вынести куда то

import uuid


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('access_token')

        if not token:
            return redirect(url_for('login'))

        try:
            data = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
            request.user = data  # Можно добавить любые данные, например, request.user['username']
        except jwt.ExpiredSignatureError:
            return redirect(url_for('login'))
        except jwt.InvalidTokenError:
            return redirect(url_for('login'))

        return f(*args, **kwargs)

    return decorated


def hai():
    return render_template('register.html')


# func for check test
def get_messages(room_id):
    # # Получаем все устаревшие сообщения
    # message_data = []
    # for key in r.scan_iter(match="room:*"):
    #     messages = r.zrange(key, 0, -1)
    #     if messages:
    #         for message in messages:
    #             message_data.append()

    # room = Room.get_room_by_id(f"{room_id}")
    # if room:
    #     print("Комната не найдена")
    # else:
    #     print("Комната не найдена")
    all = []
    all_rooms = Room.get_all_rooms()
    for r in all_rooms:
        all.append(r)
    return jsonify(all)


def create_chat():
    room_id = str(uuid.uuid4())
    return redirect(url_for('chat', room_id=room_id))


# Новый маршрут для отображения index.html
@token_required
def chat(room_id):  # добавить переход с логина в апку а не сразу в чат
    username = request.user['sub']
    update_online_status(username)
    token = request.cookies.get('access_token')
    return render_template('index.html', room_id=room_id, token=token, username=username)


# ("/users")
def get_all_users():
    users = User.find_all()
    a = [[i['username'], i['is_online']] for i in users]
    return f'{a}'

def all_del():
    client.drop_database('chat_app')
    r.flushall() # Удаляю весь редис
    return f'VSE snesli'

# -------Login------
def get_login():
    return render_template('login.html')


def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # user = User.find_by_username(f'{username}')
    user = User.verify_password(f"{username}", f"{password}")
    User.set_online(username, online=True)
    if user:
        token = User.generate_jwt(
            user["username"],
            os.getenv("SECRET_KEY")
        )
        # session['jwt_token'] = token

        # Создаем response и устанавливаем cookie
        response = make_response(jsonify({"message": "Login successful!"}), 200)
        response.set_cookie(
            'access_token',
            token,
            httponly=True,  # Защита от XSS
            secure=True,  # Только HTTPS (в продакшене)
            samesite='Lax'  # Защита от CSRF
        )

        return response
    else:
        return jsonify({"error": "Invalid credentials"}), 401


# -------Register---------
def get_register():
    return render_template('register.html')


def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Здесь должна быть логика сохранения пользователя
    print(f"New user registered: {username}")
    user = User(f"{username}", f"{password}")
    user.save()
    return jsonify({'message': f'User {username} registered successfully!'})
# -----------------
# def get_user():
#
#     user = User.find_by_username('testuser123')
#     if user:
#         return jsonify({"msg": "User found"}), 201
#     return jsonify({"msg": "User not found"}), 201
