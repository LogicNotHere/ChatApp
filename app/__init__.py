from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

from app.routes.main import hai, get_register, register, get_login, get_all_users, chat, login
from app.routes.socket import handle_message  # Импорт обработчика WebSocket

# Регистрация маршрутов
app.route("/")(hai)
app.get("/register")(get_register)  # Заглушка для  get  метода
app.post("/register")(register)
app.get("/login")(get_login)  # Заглушка для  get  метода
app.post("/login")(login)
app.route("/users")(get_all_users)
app.route("/chat")(chat)  # Новый маршрут для чата

# Регистрация обработчика WebSocket
socketio.on_event('send_message', handle_message)
