from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager


app = Flask(__name__)
login = LoginManager(app)
login.login_view = 'login'
csrf = CSRFProtect(app)
csrf.init_app(app)
app.secret_key = 'myverylongsecretkey'


from app import routes
