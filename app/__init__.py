from flask import Flask
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
csrf = CSRFProtect(app)
csrf.init_app(app)
app.secret_key = 'myverylongsecretkey'

from app import routes
