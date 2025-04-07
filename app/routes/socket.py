from flask_socketio import emit, join_room
from ..redis import add_message_to_room
from app import socketio


def handle_join(data):
    room = data.get('room')
    join_room(room)


def handle_message(data):
    username = data.get('username')
    message = data.get('message')
    room = data.get('room')

    if not username or not message or not room:
        emit('error', {'msg': 'All fields are required!'})
        return
    add_message_to_room(room, username, message)
    emit('receive_message', {'username': username, 'message': message}, room=room)

# def handle_message(data):
#     """
#     Обработчик для получения и отправки сообщений через WebSocket.
#     """
#     username = data.get('username')
#     message = data.get('message')
#
#     if not username or not message:
#         emit('error', {'msg': 'Username and message are required!'})
#         return
#
#     # Отправляем сообщение всем подключенным клиентам
#     emit('receive_message', {'username': username, 'message': message}, broadcast=True)
