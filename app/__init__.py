from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from config import Config
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flaskext.mysql import MySQL

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
#mysql = MySQL(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app.models import User, MyModelView
# For flask admin

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated
        # has role - flask security

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

admin = Admin(app, index_view = MyAdminIndexView())
admin.add_view(MyModelView(User, db.session))

from app import routes, models
