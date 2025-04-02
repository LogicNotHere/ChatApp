import redis
from datetime import datetime

r = redis.Redis(host='redis', port=6379, db=0)

def update_online_status(username):
    key = f"online:{username}"
    now = datetime.now().timestamp()
    r.setex(key, 300, now)  # TTL 5 минут (300 секунд)

def get_online_users():
    online_users = []
    for key in r.scan_iter("online:*"):
        user_id = key.decode().split(":")[1]
        timestamp = float(r.get(key))
        online_users.append((user_id, timestamp))
    return online_users