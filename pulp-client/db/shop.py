from flask_login import UserMixin

from db.db import get_db

class Shop(UserMixin):
    def __init__(self, id_, name, email, address):
        self.id_ = id_
        self.name = name
        self.email = email
        self.address = address

    @staticmethod
    def get_all():
        db = get_db()
        shops = db.execute(
            "SELECT * FROM shop"
        ).fetchall()
        if not shops:
            return None
        
        shop_list=[]
        for shop in shops :
            shop_obj = Shop(
                id_=shop[0], name=shop[1], email=shop[2], address=shop[3]
            )
            shop_list.append(shop_obj)
        return shop_list