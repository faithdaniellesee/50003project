import datetime
from app import db, login
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for, g
from passlib.hash import sha256_crypt

#flask-user implementation
from flask_user import UserManager, UserMixin, current_user
# from flask_babelex import Babel

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True) #The collation='NOCASE' is required to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(256), nullable=False, server_default='')
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    # Relationships
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password = sha256_crypt.hash(password)

    def check_password(self, password):
        return sha256_crypt.verify(password, self.password)

# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

class Tickets(db.Model):
    _tablename_ = 'tickets'
    id = db.Column(db.String(256), primary_key=True)
    options = db.Column(db.String(10))
    name = db.Column(db.String(50))
    title = db.Column(db.String(100))
    status = db.Column(db.String(10))
    isdelete = db.Column(db.String(5))
    details = db.Column(db.Text())
    upload = db.Column(db.String(256))

@login.user_loader
def load_user(id):
    return User.query.get_id(id)

class MyModelView(ModelView):
    # User can see model if it returns true
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))
