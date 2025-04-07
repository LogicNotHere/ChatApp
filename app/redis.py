import redis, json
from datetime import datetime, timezone

r = redis.Redis(host='redis', port=6379, db=0)

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

def add_message_to_room(room, username, message):
    redis_key = f"room:{room}"

    message_data = {
        'user': username,
        'text': message,
        'timestamp': datetime.now(timezone.utc)
    }

    r.hset(redis_key, f"message:{datetime.now(timezone.utc)}", json.dumps(message_data))