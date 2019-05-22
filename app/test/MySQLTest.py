import mysql.connector
import secrets

db_password = secrets.db_password

mydbtest = mysql.connector.connect(
	host = "sql12.freemysqlhosting.net",
	user = "sql12292850",
	password = db_password,
	database = "sql12292850"
)
cur = mydbtest.cursor()

Real_List = [('messages',),('roles',), ('tickets',), ('user_roles',), ('users',)]
##test for all the table in the db
def test_1 ():
	ls = []
	cur.execute("SHOW TABLES")
	for x in cur:
		ls.append(x)
	assert ls == Real_List,"Test for all existing tables : FAIL."
	print ("Test for all existing tables : PASS")
	

##test for addition of tables 
def test_2 ():
	ls = []
	Real_List.append(('ztable_test',))
	cur.execute("CREATE TABLE ztable_test (name VARCHAR(225))")
	cur.execute("SHOW TABLES")
	for x in cur:
		ls.append(x)
	assert ls == Real_List , "Test for added tables : FAIL."
	print ("Test for added tables : PASS")
	

##test for quiries code
def test_3 ():
	cur.execute("INSERT INTO ztable_test(name) VALUES ('UserTest')")
	cur.execute("SELECT name FROM ztable_test")
	result = cur.fetchall()
#	print (result[0])
	assert result[0] == ('UserTest',),"Query Test : FAIL"
	print("Query Test : PASS")

##test for deletion of tables
def test_4 ():
	ls = []
	Real_List.remove(('ztable_test',))
	cur = mydbtest.cursor()
	cur.execute("DROP TABLE ztable_test")
	cur.execute("SHOW TABLES")
	for x in cur:
		ls.append(x)
	assert ls == Real_List,"Test for deletion of tables : FAIL"
	print ("Test for deletion of tables : PASS")

##test for querying inexistent table should produce an error
def test_5 ():
	#assert ()
	try:
		cur.execute("INSERT INTO ztable_test(name) VALUES ('UserTest')")
		print("TEST : FAIL") 
	except:
		print("Trying to insert to a deleted table \nResult : Error Produced \nTest result : PASS")

test_1()
test_2()
test_3()	
test_4()
test_5()

#def ShowTables():
#	cur.execute("SHOW TABLES")
#	for x in cur:
#		print(x)

#ShowTables()
#cur.execute ("CREATE TABLE TEST1 (name VARCHAR(255))")
#ShowTables()
#cur.execute("DROP TABLE TEST1")
#ShowTables()



