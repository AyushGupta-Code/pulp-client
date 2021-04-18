from db.user import User
from flask_login import login_required
from flask import Flask, redirect, request, url_for, Blueprint
from flask_login import current_user
from werkzeug.utils import secure_filename
from pulp_config import UPLOAD_FOLDER
from db.shop import Shop
from base64 import b64encode
from db.orders import Order
import os
import random
import requests
import json

orderpage = Blueprint('orderpage', __name__, template_folder='templates')

@login_required
@orderpage.route("/dashboard/users/<userid>/orders", methods=['GET'])
def get_all(userid):
    
    create_order_button = '''<p><center><button onclick="window.location.href='/dashboard/users/{}/orders/new'">Create New Order</button></center></p>'''.format(userid)

    orders_list = Order.get(userid)

    if orders_list == None :
        return create_order_button
    
    table = '''<table style="width:100%">
            <tr>
                <th>Orderid</th>
                <th>Shopname</th>
                <th>File</th>
                <p></p>
            </tr>'''

    table_details = ""

    for order in orders_list : 
        table_row = '''<tr>
        <td><center><a href = "/dashboard/users/{}/orders/{}">{}</a></center></td>
        <td><center>{}</center></td>
        <td><center><img src="data:image/png;base64, {}" width="100" height="100"  alt="Order Image" /><center></td>
        </tr>'''.format(userid, order[0], order[0], order[1], convertToBase64(order[2]) )
        table_details += table_row
    
    logout_button = '<center><a class="button" href="/logout">Logout</a></center>'
    close_table = '</table>'
    
    
    
    return table + table_details + close_table + create_order_button + logout_button


@login_required    
@orderpage.route("/dashboard/users/<userid>/orders/new", methods=['GET'])    
def create_new(userid):
    shops = Shop.get_all()

    form = '''<center><form method="post" enctype="multipart/form-data" action = '/dashboard/users/{}/orders'>
           <div>'''.format(userid)

    file_selector = '''<p><label for="file">Choose file to upload</label></p>
                    <p>
                    <input type="file" id="file" name="file" accept="image/*,.pdf"></p>
                    </div>
                    <div>
                    <button>Submit</button>
                    </div>
                    </form>
                    <a class="button" href="/logout">Logout</a>
                    </center>''' 

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


@login_required
@orderpage.route("/dashboard/users/<userid>/orders/<orderid>", methods=['GET'])
def get(userid, orderid) :
    
    order_details = Order.get_order(orderid)

    # return_this = '''<form method="get" enctype="multipart/form-data action = '/dashboard/users/{}/orders/{}'>'''.format(userid, orderid)

    order_html =  ''' 
                    <center><p><b> Orderid : {} </b></p>
                    <p><b> Your Order : <br/> <img src="data:image/png;base64, {}" alt="Order Image" /></p></b>
                    <p><b> Status : {} </p></b>
                    <p><b> Shop : {} </p></b>
                    <button onclick="window.location.href='/dashboard/users/{}/orders'"> Show all Orders </button>
                    <p><a class="button" href="/logout">Logout</a></p></center>'''.format(
                        orderid, convertToBase64(order_details[1]),  order_details[0], order_details[2] + "," + order_details[3], userid)
    
    return order_html
    


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


def convertToBase64(image_blob) :
    enc_image = b64encode(image_blob)

    return enc_image.decode('utf-8')
