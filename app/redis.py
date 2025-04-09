import redis, json
from datetime import datetime, timezone

r = redis.Redis(host='redis', port=6379, db=0)


# -------Online------
def update_online_status(username):
    redis_key = f"online:{username}"
    now = datetime.now().timestamp()
    r.setex(redis_key, 300, now)  # TTL 5 минут (300 секунд)


def get_online_users():
    online_users = []
    for key in r.scan_iter("online:*"):
        user_id = key.decode().split(":")[1]
        timestamp = float(r.get(key))
        online_users.append((user_id, timestamp))
    return online_users


# -------Room------

def add_message_to_room(room_id, username, message):
    redis_key = f"room:{room_id}"
    timestamp = datetime.now(timezone.utc).timestamp()
    message_data = {
        'user': username,
        'text': message,
        'timestamp': datetime.now(timezone.utc).isoformat()
    }

    r.zadd(redis_key, {json.dumps(message_data): timestamp})


def get_old_messages_from_redis(room_id, time):
    try:
        return r.zrangebyscore(f"room:{room_id}", 0, time)
    except redis.RedisError as e:
        print(f"Ошибка при получении сообщений из Redis для комнаты {room_id}: {e}")
        return []
