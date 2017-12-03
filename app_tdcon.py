from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
#from data import Vendors
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, RadioField, BooleanField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from datetime import datetime, date, time
import teradata

app = Flask(__name__)

# Vendors
@app.route('/vendors')
def vendors():

    # TD connection
    udaExec = teradata.UdaExec (appName="HelloWorld", version="1.0",logConsole=False)
    session = udaExec.connect( method  ="odbc",
                               system  ="${dataSourceName}",
                               username="$$tdwallet(username)",
                               password="$$tdwallet(pw_tera)")

    vendors= session.execute("SELECT * FROM vendors").fetchall()
    if vendors > 0:
        return render_template('vendors.html', vendors=vendors)
    else:
        msg = 'No Vendors Found'
        return render_template('vendors.html', msg=msg)
    # Close connection
    cur.close()

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
