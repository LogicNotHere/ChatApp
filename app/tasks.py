from celery import Celery
from .models.user import User
from .models.room import Room
from pymongo import UpdateOne
from .redis import get_online_users
from datetime import datetime, timezone, timedelta
from .redis import r, get_old_messages_from_redis
import json
from bson import ObjectId
from .db import rooms_collection

celery = Celery(__name__, broker='redis://redis:6379/0')


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Run sync_status every N minutes

    sender.add_periodic_task(280, sync_online_status.s())
    sender.add_periodic_task(120, move_old_messages_to_mongo.s())


@celery.task
def sync_online_status():
    online_users = get_online_users()
    now = datetime.now()

    for username, timestamp in online_users:
        last_online = datetime.fromtimestamp(timestamp)
        if (now - last_online).total_seconds() < 280:
            User.set_online(username, online=True)  # last_online больше N и если больше N то был давно
        else:
            User.set_online(username, online=False)  # is_online а если его там нет?


# ------Зачем я эти функции пишу тут?-------

def deserialize_messages(raw_messages):
    messages = []
    for raw in raw_messages:
        try:
            msg = json.loads(raw.decode())
            messages.append(msg)
        except json.JSONDecodeError as e:
            print(f"Ошибка при десериализации сообщения: {e}")
    return messages


def save_messages_to_mongo(room_id, messages):
    try:
        room = Room(room_id)
        for msg in messages:
            room.add_message(msg['username'], msg['text'], msg['timestamp'])

        room.save_to_mongo()
    except Exception as e:
        print(f"Ошибка при сохранении сообщений в MongoDB для комнаты {room_id}: {e}")
# ----------------
@celery.task
def move_old_messages_to_mongo():
        time = (datetime.now() - timedelta(minutes=2)).timestamp()

        for key in r.scan_iter(match="room:*"):
            room_id = key.decode().split("room:")[1]

            # Получаем старые сообщения из Redis
            old_messages = get_old_messages_from_redis(room_id, time)

            # Если старых сообщений нет, пропускаем
            if not old_messages:
                continue

            # Десериализуем сообщения
            messages = deserialize_messages(old_messages)

            # Сохраняем сообщения в MongoDB
            save_messages_to_mongo(room_id, messages)

            # Удаляем старые сообщения из Redis
            r.zremrangebyscore(f"room:{room_id}", 0, time)


    # for msg in messages:
    #     room.add_message(msg['username'], msg['text'], msg['timestamp'])
    #
    # room.save_to_mongo()
    #
    # r.zremrangebyscore(f"room:{room_id}", 0, time)
    # # Save to MongoDB с pymongo без создание объект модели Room
    # rooms_collection.update_one(
    #     {"_id": room_id},
    #     {"$push": {"messages": {"$each": messages}}},
    #     upsert=True
    # )
