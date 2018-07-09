# https://developer.teradata.com/tools/reference/teradata-python-module

# import teradata

# udaExec = teradata.UdaExec (appName="HelloWorld", version="1.0",logConsole=True)
# session = udaExec.connect(method="odbc", system="rochetd",username="hibellm", password="$$tdwallet(pw_tera)");

# # for row in session.execute("SELECT rolename from Datahub_public.myroles"):
# #     print('This is a rolename :', row)


userid=('hibellm')
dbshortcode=('CPRD')

# #WORKS WHEN YOU HAVE ONE VALUE ONLY
# for row in session.execute("INSERT into datahub_hibellm.flasktest VALUES(?,?)",(userid,dbshortcode)):
#     print('This has been inserted :', row)

import os
from PythonTeradata import PythonTeradata

pwd_file = os.path.join(os.path.expanduser('~'), '.pwd', 'hibellm_pwd')
tdRWDS = PythonTeradata()
tdRWDS.connect(pwd_file=pwd_file, dsn="EU")


sql=("INSERT into datahub_hibellm.flasktest VALUES(%s,%s)" % userid, dbshortcode)
print(sql)
results,columns = tdRWDS.insert_or_update(sql)




# userid=('hibellm','mrmagoo','Batman')
# dbshortcode=('CPRD','ABC','XYZ')
# #HOW TO ITERATE THROUGHT THE LIST
# for row in session.executemany("INSERT into datahub_hibellm.flasktest VALUES(?,?)",(userid,dbshortcode)):
#     print('This has been inserted :', row)



    # DOES NOT WORK
    # result = cur.execute("SELECT rolename FROM Datahub_public.myroles")
    # vendors = cur.fetchall()
    # print('-------------------')
    # print(vendors)

#ANOTHER EXAMPLE
# import teradata
#
# udaExec = teradata.UdaExec ()
#
# with udaExec.connect("${dataSourceName}") as session:
#     for row in session.execute("SELECT * FROM ${db}.${vt}"):
#         print(row)

    # result = cur.execute("SELECT * FROM vendors")
    # vendors = cur.fetchall()


# udaExec.connect("${dataSourceName}", password="$$tdwallet(password_$$(tdpid)")


#Put this in a file called udaexec.ini

# Application Configuration
# [CONFIG]
# appName=PrintTableRows
# version=2
# logConsole=False
# dataSourceName=ROCHETD
# db=Datahub_hibellm
# vt=vendor
# ut=users
# dt=datasources
#
# # Default Data Source Configuration
# [DEFAULT]
# method=odbc
# charset=UTF8
#
# # Data Source Definition
# [ROCHETD]
# system=rochetd
# username=hibellm
# password=Horse123
