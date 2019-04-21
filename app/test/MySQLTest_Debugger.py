import mysql.connector
import secrets
db_password = secrets.db_password
#from Test1.py import Real_List

mydbtest = mysql.connector.connect(
	host = "sql12.freemysqlhosting.net",
	user = "sql12280733",
	password = "fUVjrQzntU",
	database = "sql12280733"
)
cur = mydbtest.cursor()

#cur.execute("DROP TABLE ztable_test")

def ShowTables():
	cur.execute("SHOW TABLES")
	for x in cur:
		print(x)	
ShowTables()
#real_list_debug = Real_List.append("atable")
#print (real_list_debug)