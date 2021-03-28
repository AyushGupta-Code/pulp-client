from flask_login import login_required, logout_user
from flask import Flask, redirect, url_for, Blueprint

logoutpage = Blueprint('logoutpage', __name__, template_folder='templates')

@logoutpage.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage.index"))
