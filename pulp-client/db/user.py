from flask_login import UserMixin

from db.db import get_db

class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic, address):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic
        self.address = address

    @staticmethod
    def get(user_id):
        db = get_db()
        user = db.execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()
        if not user:
            return None

        user = User(
            id_=user[0], name=user[1], email=user[2], profile_pic=user[3], address=user[4]
        )
        return user

    @staticmethod
    def create(id_, name, email, profile_pic, address):
        db = get_db()
        db.execute(
            "INSERT INTO user (id, name, email, profile_pic,address) "
            "VALUES (?, ?, ?, ?, ?)",
            (id_, name, email, profile_pic, address),
        )
        db.commit()
    
    @staticmethod
    def update(id_, address):
        db = get_db()
        db.execute(
            "UPDATE user "
            "SET address = ? "
            "WHERE id = ? ",
            (address, id_),
        )
        db.commit()
