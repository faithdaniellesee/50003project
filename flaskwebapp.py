from app import app, db
#The Flask application instances is called app and is a member of the app package
from app.models import User

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}
