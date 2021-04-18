from db.user import User
from flask_login import login_required
from flask import Flask, redirect, request, url_for, Blueprint
from flask_login import current_user
import requests
import json

#creates a page
userpage = Blueprint('userpage', __name__, template_folder='templates')


# userid is a variable and "users" is constant
@userpage.route("/dashboard/users/<userid>", methods=['GET'])
def get(userid):
    #here the user is verified and we have his address as well
    if current_user.is_authenticated and current_user.address :
        return (
            "<p>Hello, {}! You're logged in! Email: {} Address: {}</p>"
            "<div><p>Google Profile Picture:</p>"
            '<img src="{}" alt="Google profile pic"></img></div>'
            '<a class="button" href="/logout">Logout</a>'
            '''<p><button onclick="window.location.href='/dashboard/users/{}/orders'">Show Orders</button></p>'''.format(
                current_user.name, current_user.email, current_user.address, current_user.profile_pic, current_user.id
            
            )
        )
    #here if we dont have address, redirect to this
    elif current_user.is_authenticated :
        return (
            '''
            <form action="/dashboard/users/{}" method="post">
            <label for="address">Please Add your address to continue:</label><br>
            <input type="text" id="address" name="address"><br>
            <input type="submit" value="Submit">
            </form> '''.format(current_user.id) 
        )

    #here if we have nither authenticated user or address (cant have address if you dont have authenticated user)
    else :
        return redirect("/")

# userid is a variable and "users" is constant
@login_required
@userpage.route("/dashboard/users/<userid>", methods=['POST'])
def update(userid):
    address = request.form['address']
    User.update(userid, address)
    return redirect("/dashboard/users/" + current_user.id)
