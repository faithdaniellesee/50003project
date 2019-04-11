import mysql.connector

mydbtest = mysql.connector.connect(
	host = "sql12.freemysqlhosting.net",
	user = "sql12280733",
	password = "fUVjrQzntU",
	database = "sql12280733"
)
cur = mydbtest.cursor()

def ShowTables():
	cur.execute("SHOW TABLES")
	for x in cur:
		print(x)
cur.execute("SHOW TABLES")

ShowTables()
cur.execute ("CREATE TABLE TEST1 (name VARCHAR(255))")
cur.commit()
ShowTables()
cur.execute("DROP TABLE Tickets")



