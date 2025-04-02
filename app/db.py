from dotenv import load_dotenv
from pymongo import MongoClient
import os

from datetime import datetime, timedelta,  timezone
import jwt
from passlib.hash import pbkdf2_sha256

import redis
# Загрузка переменных окружения из .env
load_dotenv()


# redis_client = redis.Redis(host='redis', port=6379, db=0)

# Подключение к MongoDB
mongo_uri = os.getenv('MONGO_URI')
client = MongoClient(mongo_uri)
db = client['chat_app']