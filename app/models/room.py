from datetime import datetime, timezone
from bson.objectid import ObjectId


class Room:
    def __init__(self, room_id=None, messages=None):
        self.room_id = room_id or str(ObjectId())  # str(ObjectId())
        self.messages = messages or []

    def to_dict(self):
        return {
            "_id": self.room_id,
            "messages": self.messages
        }

    #@staticmethod
    def add_message(self, username, text, time): #user_id,
        message = {
            "username": username, #    надо ли мне это поле?
            "text": text,
            "timestamp": time
        }
        self.messages.append(message)