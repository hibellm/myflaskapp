from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
#from data import Vendors
from wtforms import Form, StringField, TextAreaField, PasswordField, RadioField, BooleanField, validators
from wtforms.validators import DataRequired
from passlib.hash import sha256_crypt
from functools import wraps
from datetime import datetime, date, time
import teradata
import logging
from logging.handlers import SMTPHandler
from logging import Formatter
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

#ERROR Handling
@app.errorhandler(404)
def page_not_found(error):
    return ender_template('page_not_found.html', error=error),404

#IN CASE THE LOG ON DOES NOT WORK
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('login.html', error=error),500


print('-------FLASK INFO--------')
print('STARTING THE FLASK APP...')
print('-------FLASK INFO--------')

#TERADATA CONNECTION INFOMATION - ALSO USES UDAEXEC.INI FILE IN HOME DIRECTORY
udaExec = teradata.UdaExec (appName="RU Flaskapp", version="1.0",logRetention=1,logLevel="INFO",logConsole=False,configureLogging=False)
#USED TO WRITE TO THE TABLES
tdcon = udaExec.connect(method="odbc", system="rochetd",username="hibellm", password="$$tdwallet(pw_ldap)", authentication="LDAP");

print('--------FLASK INFO---------')
print('CONNECTION TO TERADATA MADE')
print('--------FLASK INFO---------')


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
# # Register Form Class
# class RegisterForm(Form):
#     userid   = StringField('User ID', [validators.Length(min=1, max=10)])
#     email    = StringField('Email', [validators.Length(min=6, max=50)])
#     username = StringField('Username', [validators.Length(min=1, max=50)])
#     userpw   = PasswordField('Password', [
#         validators.DataRequired(),
#         validators.EqualTo('confirm', message='Passwords do not match')
#     ])
#     confirm = PasswordField('Confirm Password')

# # User Register
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegisterForm(request.form)
#     if request.method == 'POST' and form.validate():
#         userid   = form.userid.data
#         email    = form.email.data
#         username = form.username.data
#         userpw   = sha256_crypt.encrypt(str(form.userpw.data))
#
#         # ENTER THE DATA INTO A USER TABLE
#         for row in tdcon.execute("INSERT into datahub_hibellm.ru_userlist(userid, username, email, userpw) VALUES(?,?,?,?)", (userid, username, email, userpw)):
#             print('Entered the user:'+userid+' into the database')
#
#         flash('You are now registered and can log in', 'success')
#
#         return redirect(url_for('login'))
#     return render_template('register.html', form=form)

# User login
# LIST OF RUs
class RequestForm(Form):
    userid = StringField('userid', [validators.Length(min=1, max=10)])
    userpw   = PasswordField('Password', [validators.DataRequired()])

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = RequestForm(request.form)

    if request.method == 'POST' and form.validate():
        # Get Form Fields
        userid = request.form['userid']
        print(userid)

        print('len userid is:'+len(userid))
        password_candidate = request.form['userpw']
        print(password_candidate)
        print('len password_candidate is:'+len(password_candidate))
        utdcon = udaExec.connect(method="odbc", system="rochetd",username=userid, password=password_candidate, authentication="LDAP");

        # Get user by userid
        for row in utdcon.execute("SELECT USER"):
            print(row)
            # print(row[3])
            result=row

            if len(result) > 0:
                session['userid'] = userid
                print('session user id is:'+session['userid'])
                session['logged_in'] = True
                print('result found - so logged in')
                flash('You are now logged in', 'success')

                # Compare Passwords
                # if sha256_crypt.verify(password_candidate, userpwd):
                #     # Passed
                #     session['logged_in'] = True
                #     session['userid'] = result[0]
                #
                #     flash('You are now logged in', 'success')
                return redirect(url_for('ru_datasource'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
        else:
            print('len userid is:'+len(userid))
            if len(userid)<1:
                error = 'UserID not found'
                flash('No userid found','danger')
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
    dbid        = StringField('dbid',)

# Dashboard of RU
@app.route('/ru_datasource',methods=['GET', 'POST'])
@is_logged_in
def ru_datasource():
    form = rudatasourceForm(request.form)

    # Get list of RU
    cur=tdcon.execute("select a.dbid,a.dbshortcode,pdflink,approval,userid,requestdate,requested,granteddate,granted "+
                      "from (SELECT dbid,dbshortcode,pdflink,approval FROM datahub_hibellm.ru_list) as a "+
                      "left join (SELECT * FROM datahub_hibellm.ru_registry where userid='"+session['userid']+"') as b on a.dbshortcode=b.dbshortcode;")
    datasource= cur.fetchall()

    # Get datasourcelist
    if len(datasource) > 0:
        return render_template('ru_datasource.html', form=form,datasource=datasource)
    else:
        msg = 'No R&amp;U Found...strange'
        return render_template('ru_datasource.html', msg=msg,form=form)

# Log a Request for access
@app.route('/request_access/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def logrequest(id):
    # CHECK IF ALREADY APPPLIED?
    tst=tdcon.execute("SELECT '1' FROM datahub_hibellm.ru_registry WHERE dbid = ? and userid = ?", (id,session['userid']) )
    mjh = str(tst.fetchall())
    # print('mjh type is',type(mjh))
    # print('length of mjh is :',len(mjh))

    if len(mjh)>2:
        flash('Already have access to the DataSource (or it is still Pending)', 'success')
        return redirect(url_for('ru_datasource'))
    else:
        print('Data Source not yet requested so continuing')

        # cur=tdcon.execute("SELECT * FROM datahub_hibellm.ru_list WHERE dbid= ?", (id))
        cur=tdcon.execute("SELECT * FROM datahub_hibellm.ru_list WHERE dbid='"+id+"'")
        logrequest = cur.fetchall()
        # print('-------FLASK INFO--------(LOGREQUEST)--START')
        # print('The ID wanted is:'+id)
        # print('The results are:')
        # print(logrequest)
        # print(type(logrequest))
        # print('-------FLASK INFO--------(LOGREQUEST)--END')

        form = rudatasourceForm(request.form)

        if request.method == 'POST' and form.validate():
            dbid        = form.dbid.data
            dbshortcode = form.dbshortcode.data
            agree       = form.agree.data
            dttime      = datetime.now()

            # print('The value of agree is :'+str(agree))
            # Check if agree ticked
            if agree == 1:
                print('The user agreed to datasource :'+ dbshortcode)
                cur=tdcon.execute("INSERT INTO datahub_hibellm.ru_registry(userid,dbid,dbshortcode,requestdate,requested) VALUES(?,?,?,?,?)",(session['userid'],dbid,dbshortcode,dttime,int(agree)))

                flash('DataSource ' + dbshortcode +' Access requested', 'success')
                return redirect(url_for('ru_datasource'))
            else:
                flash('You have not ticked the "Agree". ' + dbshortcode +' Access not requested', 'danger')
                # return redirect(url_for('request_access'))
                return render_template('/request_access.html', form=form, logrequest=logrequest )
        return render_template('/request_access.html', form=form, logrequest=logrequest )

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run('0.0.0.0', 5003, debug=False)
