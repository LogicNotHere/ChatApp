from celery import Celery
from .models.user import User
from .redis import get_online_users
from datetime import datetime

celery = Celery(__name__, broker='redis://redis:6379/0')


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Запускать sync_status каждые 5 минут
    sender.add_periodic_task(280, sync_online_status.s())


@celery.task
def sync_online_status():
    online_users = get_online_users()
    now = datetime.now()

    for username, timestamp in online_users:
        last_online = datetime.fromtimestamp(timestamp)
        # Если активность была в последние 5 минут - пользователь онлайн
        if (now - last_online).total_seconds() < 280:
            User.set_online(username, online=True)  # last_online больше N и если больше N то был давно
        else:
            User.set_online(username, online=False)  # is_online

@celery.task
def save_message_to_mongo():
    pass