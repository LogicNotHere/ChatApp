from flask import jsonify, render_template, request, redirect, url_for, session, make_response
from ..models.user import User
from ..redis import update_online_status
import os

from ..db import jwt  # вынести куда то
from functools import wraps  # вынести куда то


def token_required(f):  # вынести куда то decorator
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('access_token')

        if not token:
            return redirect(url_for('login'))  # Редирект, если нет токена

        try:
            # Проверяем токен
            data = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
            # Можно добавить данные в `request` (например, request.user = data)
        except jwt.ExpiredSignatureError:
            return redirect(url_for('login'))  # Токен просрочен
        except jwt.InvalidTokenError:
            return redirect(url_for('login'))  # Токен невалиден

        return f(*args, **kwargs)

    return decorated


def hai():
    return render_template('register.html')


# Новый маршрут для отображения index.html
@token_required
def chat():  # добавить переход с логина в апку а не сразу в чат
    update_online_status("Sula61")  # взять имя с ДЖвт токена
    return render_template('index.html')


# ("/users")
def get_all_users():
    users = User.find_all()
    a = [i['is_online'] for i in users]
    return f'{a}'


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
