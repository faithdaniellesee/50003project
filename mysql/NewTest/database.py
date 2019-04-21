# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 02:31:02 2019

@author: user
"""

from flask import Flask
from flaskext.mysql import MySQL

app = Flask(__name__)
app.config['MYSQL_DATABASE_HOST'] = 'sql12.freemysqlhosting.net' 
app.config['MYSQL_DATABASE_USER'] = 'sql12280733' 
app.config['MYSQL_DATABASE_DB'] = 'sql12280733'
#app.config['MYSQL_DATABASE_PORT'] = '3306'

mysql = MySQL()
mysql.init_app(app)

@app.route('/')
def index():
    cur = mysql.get_db().cursor()
    cur.execute('''SELECT data FROM StartingNew WHERE id = 1''')
    rv = cur.fetchall()
    return str(rv)
    
if __name__ == '__main__':
    app.run(debug=True)
