from flask_login import UserMixin

from db.db import get_db

class Order(UserMixin) :
    def __init__(self, orderid, status, image_file, shopid, user_id):
        self.orderid = orderid
        self.status = status
        self.img_file = image_file
        self.shopid = shopid
        self.user_id = user_id
    

    @staticmethod
    def get(user_id) : 
        db = get_db()
        orders = db.execute(
            "SELECT orders.orderid, shop.shop_name, orders.file  FROM orders INNER JOIN shop ON orders.shopid = shop.shopid WHERE orders.userid = ?", (user_id,)
        ).fetchall()
        if not orders:
            return None
        
        return orders

    @staticmethod
    def create(orderid, status, image_file, shopid, user_id) :
        db = get_db()
        db.execute (
            "INSERT INTO orders (orderid, file, shopid, status, userid) "
            "VALUES (?, ?, ?, ?, ?)",
            (orderid, image_file, shopid, status, user_id),
        )
        db.commit()

    @staticmethod
    def get_order(orderid):
        db = get_db()
        orders = db.execute(
            '''SELECT orders.status, orders.file, shop.shop_name, shop.shop_address 
            FROM  orders 
            INNER JOIN shop 
            ON shop.shopid = orders.shopid  
            WHERE orders.orderid = ?''', (orderid,)
        ).fetchone()

        return orders

    
