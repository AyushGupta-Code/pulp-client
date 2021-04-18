from db.user import User
from flask_login import login_required
from flask import Flask, redirect, request, url_for, Blueprint
from flask_login import current_user
from werkzeug.utils import secure_filename
from pulp_config import UPLOAD_FOLDER
from db.shop import Shop
from db.orders import Order
import os
import random
import requests
import json

orderpage = Blueprint('orderpage', __name__, template_folder='templates')

@login_required
@orderpage.route("/dashboard/users/<userid>/orders", methods=['GET'])
def get_all(userid):
    return ( 
        '''<p><button onclick="window.location.href='/dashboard/users/{}/orders/new'">Create New Order</button></p>'''.format(userid)
    )

@login_required    
@orderpage.route("/dashboard/users/<userid>/orders/new", methods=['GET'])    
def create_new(userid):
    shops = Shop.get_all()

    form = '''<form method="post" enctype="multipart/form-data" action = '/dashboard/users/{}/orders' >
           <div>'''.format(userid)

    file_selector = '''<p><label for="file">Choose file to upload</label></p>
                    <p>
                    <input type="file" id="file" name="file" accept="image/*,.pdf"></p>
                    </div>
                    <div>
                    <button>Submit</button>
                    </div>
                    </form>''' 

    all_options = ""
    for shop in shops :
        option = '''<option value = "{}"> {}</option>'''.format(shop.id_, shop.name + ", " + shop.address)
        all_options += option
    select = '''<label for="shop">Choose a shop:</label>
             <select name="shop" id="shop">'''
    select_close = '''</select>'''

    return form + select + all_options + select_close + file_selector



@login_required
@orderpage.route("/dashboard/users/<userid>/orders", methods=['POST'])
def create(userid):
    shopid = request.form['shop']
    image_file = request.files['file']
    if image_file :
        filename = secure_filename(image_file.filename)
        image_file_path = os.path.join(UPLOAD_FOLDER, filename)
        image_file.save(image_file_path)

        image_blob = convertToBinaryData(image_file_path)
        orderid = random.randint(0,999999)
        Order.create(orderid, 'PENDING', image_blob, shopid, userid)
    
    return redirect("/dashboard/users/{}/orders/{}".format(userid, orderid))


# @orderpage.route("/dashboard/users/<userid>/orders/<orderid>", methods=['GET'])
# def get(userid, orderid) :
#     order=Order.get_order(orderid)
    



#     #make a html page that returns file(image),shop name, orderid
#     return "Order Values"
    


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData



