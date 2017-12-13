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
udaExec = teradata.UdaExec (appName="RU Flaskapp", version="1.0",logRetention=1,logLevel="ERROR",logConsole=True)
tdcon = udaExec.connect(method="odbc", system="rochetd",username="hibellm", password="$$tdwallet(pw_tera)");

# Index
@app.route('/')
def index():
    print('Website is running....')
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
        for row in tdcon.execute("INSERT into datahub_hibellm.ru_userlist(userid, username, email, userpw) VALUES(?,?,?,?)", (userid, username, email, userpw)):
            print('Entered the user:'+userid+' into the database')

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

        # Get user by userid
        for row in tdcon.execute("SELECT * FROM datahub_hibellm.ru_userlist WHERE userid = ?", [userid]):
            print(row)
            print(row[3])
            result=row
        # print(dir(result))

        if len(result) > 0:
            # Get stored hash
            userpwd = result[3]

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, userpwd):
                # Passed
                session['logged_in'] = True
                session['userid'] = result[0]

                flash('You are now logged in', 'success')
                return redirect(url_for('ru_datasource'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
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


# LIST OF RUs
class rudatasourceForm(Form):
    dbshortcode = StringField('DBShortCode', [validators.Length(min=1, max=10)])
    agree       = BooleanField('I agree.', )

# Dashboard of RU
@app.route('/ru_datasource',methods=['GET', 'POST'])
@is_logged_in
def ru_datasource():
    form = rudatasourceForm(request.form)


 # Try this!!!! https://stackoverflow.com/questions/37850181/python-pytd-teradata-query-into-pandas-dataframe

    # Get status list of RU
    # for row in tdcon.execute("select * from (SELECT dbid,dbshortcode,pdflink,approval FROM datahub_hibellm.ru_list) as a left join (SELECT * FROM datahub_hibellm.ru_registry where userid='?') as b on a.dbshortcode=b.dbshortcode;", session['userid']):
    # for row in tdcon.execute("select * from (SELECT dbid,dbshortcode,pdflink,approval FROM datahub_hibellm.ru_list) as a left join (SELECT * FROM datahub_hibellm.ru_registry where userid='hibellm') as b on a.dbshortcode=b.dbshortcode;"):
    #     datasource=row
    #     print(datasource)

    cur=tdcon.execute("select * from (SELECT dbid,dbshortcode,pdflink,approval FROM datahub_hibellm.ru_list) as a left join (SELECT * FROM datahub_hibellm.ru_registry where userid='hibellm') as b on a.dbshortcode=b.dbshortcode;")
    datasource= cur.fetchall()
    # for rowMetaData in cur.description:
    #      cols.append(rowMetaData[0])
    #      df.columns = cols
    #      print(df.columns)
    # for row in cur:
    #      datasource=row
    #      print(datasource)


    # Get datasourcelist
    if len(datasource) > 0:
        return render_template('ru_datasource.html', datasource=datasource,form=form)
    else:
        msg = 'No R&amp;U Found...strange'
        return render_template('ru_datasource.html', msg=msg ,form=form)

#Request Rand U
@app.route('/request_access')
def request_access(id):

    # cur=tdcon.execute("select * from (SELECT dbid,dbshortcode,pdflink,approval FROM datahub_hibellm.ru_list) as a left join (SELECT * FROM datahub_hibellm.ru_registry where userid='hibellm') as b on a.dbshortcode=b.dbshortcode;")
    # datasource= cur.fetchall()
    result = cur.execute("SELECT * FROM datahub_hibellm.ru_list WHERE dbid = ?", [id])
    datasource = cur.fetchone()
    return render_template('request_access.html', datasource=datasource)

# Log a Request for access
@app.route('/request_access/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def logrequest(id):
    form = rudatasourceForm(request.form)
    if request.method == 'POST' and form.validate():
        dbshortcode = form.dbshortcode.data
        agree       = form.agree.data
        dttime      = datetime.now()

        print('The value of agree is :'+agree)
        # Check if agree ticked
        if agree == 1:
            print('The user aggreed to datasource :'+ dbshortcode)
            # cur.execute("INSERT INTO ru_registry(userid,dbshortcode,requestdate,request) VALUES(%s,%s,%s,%s)",(session['username'],dbshortcode,dttime,agree))
            cur=tdcon.execute("INSERT INTO datahub_hibellm.ru_registry(userid,dbshortcode,requestdate,request) VALUES(?,?,?,?)",(session['userid'],dbshortcode,dttime,agree))
            # datasource= cur.fetchall()

            flash('DataSource ' + dbshortcode +' Access requested', 'success')
            # return redirect(url_for('/request_access/<string:id>'))
            return redirect(url_for('ru_datasource'))
        else:
            flash('You have not ticked the "Agree". ' + dbshortcode +' Access not requested', 'danger')
            # return redirect(url_for('/request_access/<string:id>'))
            return redirect(url_for('/request_access/<string:id>'))

    return render_template('ru_datasource.html', form=form)



if __name__ == '__main__':
    app.secret_key='secret123'
    app.run('0.0.0.0',5003,debug=True)
