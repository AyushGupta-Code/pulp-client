from flask_login import current_user
from flask import Blueprint

homepage = Blueprint('homepage', __name__, template_folder='templates')

@homepage.route('/')
def index():
    if current_user.is_authenticated:
        return (
            "<p>Hello, {}! You're logged in! Email: {} Address: {}</p>"
            "<div><p>Google Profile Picture:</p>"
            '<img src="{}" alt="Google profile pic"></img></div>'
            '<a class="button" href="/logout">Logout</a>'.format(
                current_user.name, current_user.email, current_user.address, current_user.profile_pic
            )
        )
    else:
        return '''<div class="col s12 m6 offset-m3 center-align">
    <a class="oauth-container btn darken-4 white black-text" href="/login" style="text-transform:none">
        <div class="left">
            <img width="20px" style="margin-top:7px; margin-right:8px" alt="Google sign-in" 
                src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/512px-Google_%22G%22_Logo.svg.png" />
        </div>
        Login with Google
    </a>
</div>

<!-- Compiled and minified CSS -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/css/materialize.min.css">

<!-- Compiled and minified JavaScript -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/js/materialize.min.js"></script>
'''
