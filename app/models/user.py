from ..db import db, pbkdf2_sha256, datetime, timedelta, jwt, timezone


class User:
    def __init__(self, username, password=None):
        self.username = username
        # self.email = email
        self.password = pbkdf2_sha256.hash(password) if password else None
        self.is_online = False

    def save(self):
        db.users.insert_one({
            "username": self.username,
            "password": self.password,
            "is_online": self.is_online
        })
        #"last_online": self.last_online

        # "email": self.email,asd
    @staticmethod
    def verify_password(username, password):
        user = User.find_by_username(username)
        if user and pbkdf2_sha256.verify(password, user["password"]):
            return user
        return None

# ------------------------Base-methods--------------------------------------
    @staticmethod
    def find_by_username(username):
        return db.users.find_one({"username": username})

    @staticmethod
    def find_all():
        return list(db.users.find())


# ------------------------JWT--------------------------------------
    @staticmethod
    def generate_jwt(username, secret_key, expires_in=3600):                     # фул хуйня зачем я это тут делаю?
        payload = {
            "sub": username,
            "exp": datetime.now(timezone.utc) + timedelta(seconds=expires_in)
        }
        return jwt.encode(payload, secret_key, algorithm="HS256")

#------------------------redis--------------------------------------

    @classmethod
    def set_online(cls, username, online):
        result = db.users.update_one(
            {"username": username},
            {"$set": {"is_online": online}}
        )
        return result.modified_count > 0