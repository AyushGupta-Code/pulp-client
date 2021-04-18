from flask_login import current_user
from flask import Blueprint
from flask import redirect

homepage = Blueprint('homepage', __name__, template_folder='templates')


#when user is authenticated, it'll show addressbox, if not it'll redirect to login page.
@homepage.route('/')
def index():
    if not current_user.is_authenticated:
        
        return '''<div top: 50%; class="col s12 m6 offset-m3 center-align">
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
    else :
        return redirect("/dashbord/users/" + current_user.id)


