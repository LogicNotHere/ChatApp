from flask_socketio import emit
from app import socketio

def handle_message(data):
    """
    Обработчик для получения и отправки сообщений через WebSocket.
    """
    username = data.get('username')
    message = data.get('message')

    if not username or not message:
        emit('error', {'msg': 'Username and message are required!'})
        return

    # Отправляем сообщение всем подключенным клиентам
    emit('receive_message', {'username': username, 'message': message}, broadcast=True)