from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
#from data import Vendors
from wtforms import Form, StringField, TextAreaField, PasswordField, RadioField, BooleanField, validators
from wtforms.validators import DataRequired
from passlib.hash import sha256_crypt
from functools import wraps
from datetime import datetime, date, time
import teradata


app = Flask(__name__)

#TERADATA CONNECTION INFOMATION - ALSO USES UDAEXEC.INI FILE IN HOME DIRECTORY
udaExec = teradata.UdaExec (appName="RU Flaskapp", version="1.0",logConsole=True)
#session = udaExec.connect(method="odbc", system="rochetd",username="$$tdwallet(username)", password="$$tdwallet(pw_tera)");
session = udaExec.connect(method="odbc", system="rochetd",username="hibellm", password="$$tdwallet(pw_tera)");

# Index
@app.route('/')
def index():
    return render_template('home.html')

# About
@app.route('/about')
def about():
    return render_template('about.html')


#LOGIN/REGISTER FUNCTIONS
# Register Form Class
class RegisterForm(Form):
    userid   = StringField('User ID', [validators.Length(min=1, max=10)])
    email    = StringField('Email', [validators.Length(min=6, max=50)])
    username = StringField('Username', [validators.Length(min=1, max=50)])
    userpw   = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        userid   = form.userid.data
        email    = form.email.data
        username = form.username.data
        userpw   = sha256_crypt.encrypt(str(form.userpw.data))

        # ENTER THE DATA INTO A USER TABLE
        for row in session.execute("INSERT into datahub_hibellm.userlist(userid, username, email, userpw) VALUES(?,?,?,?)", (userid, username, email, userpw)):
            print('Entered the user:'+userid+' into the database')

        # # Create cursor
        # cur = mysql.connection.cursor()
        # # Execute query
        # cur.execute("INSERT INTO users(name, email, username, password) VALUES(?,?,?,?)", (name, email, username, password))
        # # Commit to DB
        # mysql.connection.commit()
        # # Close connection
        # cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        userid = request.form['userid']
        password_candidate = request.form['userpw']

        # Create cursor
        #cur = mysql.connection.cursor()
        # Get user by username
        #result = cur.execute("SELECT * FROM users WHERE userid = ?", [userid])
        for row in session.execute("SELECT * FROM datahub_hibellm.userlist WHERE userid = ?", [userid]):
            result=row

        if result > 0:
            # Get stored hash
            data = row.fetchone()[0]
            userpw = data['userpw']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, userpw):
                # Passed
                session['logged_in'] = True
                session['userid'] = userid

                flash('You are now logged in', 'success')
                return redirect(url_for('about'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            # cur.close()
        else:
            error = 'UserID not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.secret_key='secret123'
    app.run('0.0.0.0',5003,debug=True)
