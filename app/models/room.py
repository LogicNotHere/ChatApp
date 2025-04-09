from datetime import datetime, timezone
from bson.objectid import ObjectId
from ..db import db, rooms_collection

class Room:
    def __init__(self, room_id=None, messages=None):
        self.room_id = room_id or str(ObjectId())  # str(ObjectId())
        self.messages = messages or []

    def to_dict(self):
        return {
            "_id": self.room_id,
            "messages": self.messages
        }

    def add_message(self, username, text, time): #user_id,
        message = {
            "username": username,
            "text": text,
            "timestamp": time
        }
        self.messages.append(message)

    def save_to_mongo(self):
        rooms_collection.update_one(
            {"_id": self.room_id},
            {"$push": {"messages": {"$each": self.messages}}},
            upsert=True
        )
        self.messages = []

    @staticmethod
    def get_room_by_id(room_id):
        room = rooms_collection.find_one({"_id": room_id})
        if room:
            return room
        return None

    @staticmethod
    def get_all_rooms():
        return list(rooms_collection.find())