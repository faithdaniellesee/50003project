from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
login = LoginManager(app)
login.login_view = 'login'
csrf = CSRFProtect(app)
csrf.init_app(app)
app.secret_key = 'myverylongsecretkey'


from app import routes, models
