# R&U App

<img src="/assets/images/book.png" width="64px" height="64px">
Simple application to register a users aknolwedgement of a "Read & understand" document.
Based off the backend database entry, access can then be granted.

This is forked from https://github.com/bradtraversy/myflaskapp (with authentication and CRUD functionality using the Python Flask micro-framework) and adapted.

## Installation

To use this template, your computer needs:

- [Python 2 or 3](https://python.org)
- [Pip Package Manager](https://pypi.python.org/pypi)

### Database

The app uses a Teradata database in the background.
Update to add in a MySQL/mongoDB connection as well. This can then be used fro reference of how to use different databases in the backend.

### To Do

- [] Update the Teradata connection code to use the TeradataPython module
- [] Clean up code and unused files (I used this area as a testing ground)
- [] Add a MySQL and MongoDB version.
- [] I'm sure there is something else I wanted to do....
- [] Change all code to work 100% off the Semantic-UI ('cos I like it)

### Running the app

```python
python3 app_tdcon_ldap.py    #Using Teradata module
python3 app_tdcon_rest.py    #Using REST API
python3 app_tdcon_tdRWDS.py  #Using PythonTeradata
```

### REF Directory structure
created by running on windows cmd line  `tree /F /A > tree.txt`

````
Folder PATH listing for volume RWD_SHARE
Volume serial number is 000000A9 2DFC:DDD8
F:.
|   README.md
|   data.pyc
|   td_python.py #to delete?
|   td_python_connection.py #to delete?
|   setup_code.sql #to delete?
|   app_tdcon_alt.py 
|   TD_conn_test_pyodbcy.py
|   migrate_code.sql #to delete?
|   app_tdcon_rest.py
|   app_tdcon_ldap.py
|   app_tdcon_old.py
|   app_tdcon_tdRWDS.py
|   tree.txt
|   
+---__pycache__
|       app.cpython-36.pyc
|       osscript.cpython-36.pyc
|       
+---templates
|   |   about.html
|   |   layout.html
|   |   login.html
|   |   register.html
|   |   roles.html
|   |   ru_datasource.html
|   |   request_access.html
|   |   page_not_found.html
|   |   internal_server_error.html
|   |   home.html
|   |   
|   \---includes
|           _formhelpers.html
|           _messages.html
|           _navbar.html
|           
\---assets
    |   favicon2.ico
    |   favicon.ico
    |   
    +---images
    |       book.png
    |       
    +---css
    \---js
            tablesort.js            
````
