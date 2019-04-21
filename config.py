import os
from flaskext.mysql import MySQL
from app import secrets
db_password = secrets.db_password
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI =  'mysql://sql12280733:'+ db_password + '@sql12.freemysqlhosting.net/sql12280733'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
     #   'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = '/home'
    USER_ENABLE_EMAIL = False
    USER_ENABLE_USERNAME = False
    USER_LOGIN_URL = '/home'
    USER_LOGIN_TEMPLATE = '/index.html'

    # Flask-Mail SMTP server settings
    '''
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'email@example.com'
    MAIL_PASSWORD = 'password'
    MAIL_DEFAULT_SENDER = '"MyApp" <noreply@example.com>'
    
    # Flask-User settings
    USER_APP_NAME = "Accenture Customer Support System"      # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = True        # Enable email authentication
    USER_ENABLE_USERNAME = True     # Enable username authentication
    USER_EMAIL_SENDER_NAME = USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = "noreply@example.com"

    '''
    # collation = "NOCASE"
    # USER_IFIND_MODE = 'nocase_collation'

#    MYSQL_DATABASE_HOST = 'sql12.freemysqlhosting.net'
#    MYSQL_DATABASE_USER = 'sql12280733'
#    MYSQL_DATABASE_PASSWORD ='fUVjrQzntU'
#    MYSQL_DATABASE_DB = 'sql12280733'

