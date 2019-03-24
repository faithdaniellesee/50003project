import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    #SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #    'sqlite:///' + os.path.join(basedir, 'app.db')
    #SQLALCHEMY_TRACK_MODIFICATIONS = False
    #Configuration of db by Billio
    MYSQL_DATABASE_HOST = 'sql12.freemysqlhosting.net' 
    MYSQL_DATABASE_USER = 'sql12280733' 
    MYSQL_DATABASE_PASSWORD ='fUVjrQzntU'
    MYSQL_DATABASE_DB = 'sql12280733'