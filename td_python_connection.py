#https://developer.teradata.com/blog/odbcteam/2016/02/python-with-teradata-odbc

# import pyodbc module
import pyodbc

# disable connection pooling
pyodbc.pooling = False
# create connection
connection = pyodbc.connect('DSN=rochetd;UID=hibellm;PWD=Horse123')
# enable auto commit
connection.autocommit = True;

# print driver and database info
print '-ODBC version        =',connection.getinfo(10)
print '-DBMS name           =',connection.getinfo(17)
print '-DBMS version        =',connection.getinfo(18)
print '-Driver name         =',connection.getinfo(6)
print '-Driver version      =',connection.getinfo(7)
print '-Driver ODBC version =',connection.getinfo(77)

# create cursor
cursor = connection.cursor()

# Does table 'employee' exist?
if cursor.tables(table='employee').fetchone():

# drop employee table
cursor.execute("drop table employee");

# create employee table
cursor.execute("CREATE SET TABLE employee (employee_number INTEGER NOT NULL PRIMARY KEY, last_name VARCHAR(50) NOT NULL, first_name VARCHAR(50) NOT NULL)");

# populate employee table with sample data
cursor.execute("INSERT INTO employee VALUES (2, 'Olson', 'Chuck')");
cursor.execute("INSERT INTO employee VALUES (3, 'Lee', 'Bill')");
cursor.execute("INSERT INTO employee VALUES (4, 'Chapman', 'Lisa')");
cursor.execute("INSERT INTO employee VALUES (1, 'Miller', 'Susan');");

#disconnect
connection.close()
