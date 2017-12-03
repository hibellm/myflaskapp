# https://developer.teradata.com/tools/reference/teradata-python-module

import teradata

udaExec = teradata.UdaExec (appName="HelloWorld", version="1.0",logConsole=False)

session = udaExec.connect(method="odbc", system="rochetd",username="hibellm", password="Horse123");

for row in session.execute("SELECT GetQueryBand()"):
    print(row)

#ANOTHER EXAMPLE
import teradata

udaExec = teradata.UdaExec ()

with udaExec.connect("${dataSourceName}") as session:
    for row in session.execute("SELECT * FROM ${db}.${vt}"):
        print(row)

    # result = cur.execute("SELECT * FROM vendors")
    # vendors = cur.fetchall()


# udaExec.connect("${dataSourceName}", password="$$tdwallet(password_$$(tdpid)")


#Put this in a file called udaexec.ini

# Application Configuration
[CONFIG]
appName=PrintTableRows
version=2
logConsole=False
dataSourceName=ROCHETD
db=Datahub_hibellm
vt=vendor
ut=users
dt=datasources

# Default Data Source Configuration
[DEFAULT]
method=odbc
charset=UTF8

# Data Source Definition
[ROCHETD]
system=rochetd
username=hibellm
password=Horse123
