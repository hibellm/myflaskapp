# import pyodbc module
import pyodbc

# disable connection pooling
pyodbc.pooling = False

# create connection
connection = pyodbc.connect('DSN=testdsn;DBCNAME=rochetd;UID=hibellm;PWD=$tdwallet(pw_ldap);Authentication=LDAP')
connection.setencoding(encoding='utf-8')
#connection.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')

# print driver and database info
print('-ODBC version        =',connection.getinfo(10))
print('-DBMS name           =',connection.getinfo(17))
print('-DBMS version        =',connection.getinfo(18))
print('-Driver name         =',connection.getinfo(6))
print('-Driver version      =',connection.getinfo(7))
print('-Driver ODBC version =',connection.getinfo(77))

# create cursor
cursor = connection.cursor()

# execute SQL statement
cursor.execute("SELECT * from DBC.DBCInfoV")

# fetch result set rows
for row in cursor:
    print(row)

# close cursor
cursor.close()

# disconnect
connection.close()
