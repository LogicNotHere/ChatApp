from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

from app.routes.main import hai, get_register, register, get_login, get_all_users, chat, login, create_chat,get_messages
from app.routes.socket import handle_message, handle_join  # Импорт обработчика WebSocket

# Регистрация маршрутов
app.route("/")(hai)

app.get("/register")(get_register)  # Заглушка для  get  метода
app.post("/register")(register)
app.get("/login")(get_login)  # Заглушка для  get  метода
app.post("/login")(login)

app.route("/users")(get_all_users)

app.route("/chat/<room_id>")(chat)  # Новый маршрут для чата
app.route('/create_chat')(create_chat)

app.route('/test/<room_id>')(get_messages)

# Регистрация обработчика WebSocket
socketio.on_event('send_message', handle_message)
socketio.on_event('join', handle_join)

