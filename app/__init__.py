import datetime
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from config import Config
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flaskext.mysql import MySQL
from passlib.hash import sha256_crypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

#flask-user implementation
from flask_user import UserManager
# from flask_babelex import Babel

app = Flask(__name__)
app.config.from_object(Config)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["2000 per hour"]
)

#babel = Babel(app)
db = SQLAlchemy(app)
#mysql = MySQL(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
app.jinja_env.autoescape = True

from app.models import User, Role, UserRoles, MyModelView

user_manager = UserManager(app, db, User) #initialize flask-user implementation

# database creation and user addition
# Create all database tables
db.create_all()

# Create 'member@example.com' user with no roles
if not User.query.filter(User.email == 'member@example.com').first():
    user = User(
        username = 'member',
        email='member@example.com',
        email_confirmed_at=datetime.datetime.utcnow(),
        password=sha256_crypt.hash('Password1'),
    )
    db.session.add(user)
    db.session.commit()

# Create 'admin@example.com' user with 'admin' roles

if not User.query.filter(User.email == 'admin@example.com').first():
    user = User(
        username = 'admin',
        email='admin@example.com',
        email_confirmed_at=datetime.datetime.utcnow(),
        password=sha256_crypt.hash('Password1'),
    )
    user.roles.append(Role(name='admin'))
    db.session.add(user)
    db.session.commit()

# flask-admin implementation
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        # return current_user.is_authenticated
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

admin = Admin(app, index_view = MyAdminIndexView())
admin.add_view(MyModelView(User, db.session))

from app import routes, models
