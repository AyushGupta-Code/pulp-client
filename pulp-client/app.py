# Python standard libraries
import json
import os
import sqlite3

from flask import Flask
from handlers.homepage import homepage
from handlers.login import loginpage
from handlers.logout import logoutpage
from handlers.user import userpage
from handlers.orders import orderpage

# Third-party libraries
from flask_login import (
    LoginManager
)

from db.db import init_db_command
from db.user import User

# Naive database setup
# try:
#     init_db_command()
# except sqlite3.OperationalError:
#     print ('Error in initializing database.')


if __name__ == "__main__":
    # Flask app setup
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

    # User session management setup
    # https://flask-login.readthedocs.io/en/latest
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Flask-Login helper to retrieve a user from our db
    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    #register different parts of your website from different files
    app.register_blueprint(homepage)
    app.register_blueprint(loginpage)
    app.register_blueprint(logoutpage)
    app.register_blueprint(userpage)
    app.register_blueprint(orderpage)
    app.run(ssl_context="adhoc")


