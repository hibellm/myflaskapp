from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
#from data import Vendors
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, RadioField, BooleanField, validators
from wtforms.validators import DataRequired
from passlib.hash import sha256_crypt
from functools import wraps
from datetime import datetime, date, time

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)

# Index
@app.route('/')
def index():
    return render_template('home.html')

# About
@app.route('/about')
def about():
    return render_template('about.html')

# ROLE SELECTOR FORM
class RoleForm(Form):
    selrole = StringField('selrole')

# Roles
@app.route('/roles', methods=["GET","POST"])
def roles():
    form = RoleForm(request.form)

    if request.method == 'POST' and form.validate():
        selrole = form.selrole.data

    # Create cursor
    cur = mysql.connection.cursor()
    # Get roles
    result = cur.execute("SELECT * FROM rwd_meta_mdh.accessroles")
    roles = cur.fetchall()
    # Get Roles for Dropdown
    result = cur.execute("SELECT * FROM rwd_meta_mdh.accessroles group by rolename")
    rolesdd = cur.fetchall()

    if result > 0:
        return render_template('roles.html', roles=roles, rolesdd=rolesdd, form=form)
    else:
        msg = 'No Data/Roles Found'
        return render_template('roles.html', msg=msg)
    # Close connection
    cur.close()



# Vendors
@app.route('/vendors')
def vendors():
    # Create cursor
    cur = mysql.connection.cursor()
    # Get vendors
    result = cur.execute("SELECT * FROM vendors")
    vendors = cur.fetchall()

    if result > 0:
        return render_template('vendors.html', vendors=vendors)
    else:
        msg = 'No Vendors Found'
        return render_template('vendors.html', msg=msg)
    # Close connection
    cur.close()

#Single Vendor
@app.route('/vendor/<string:id>/')
def vendor(id):
    # Create cursor
    cur = mysql.connection.cursor()
    # Get vendor
    result = cur.execute("SELECT * FROM rwd_meta_mdh.accessroles WHERE roleaccessid = %s", [id])
    vendor = cur.fetchone()
    return render_template('vendor.html', vendor=vendor)

######
# datasources
@app.route('/datasources')
def datasources():
    # Create cursor
    cur = mysql.connection.cursor()
    # Get datasources
    result = cur.execute("SELECT * FROM datasources")
    datasources = cur.fetchall()

    if result > 0:
        return render_template('datasources.html', datasources=datasources)
    else:
        msg = 'No datasources Found'
        return render_template('datasources.html', msg=msg)
    # Close connection
    cur.close()


#Single datasource
@app.route('/datasource/<string:id>/')
def datasource(id):
    # Create cursor
    cur = mysql.connection.cursor()
    # Get vendor
    result = cur.execute("SELECT * FROM datasources WHERE id = %s", [id])
    datasource = cur.fetchone()
    return render_template('datasource.html', datasource=datasource)


# Register Form Class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

#LOGIN/REGISTER FUNCTIONS
# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = mysql.connection.cursor()
        # Execute query
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))
        # Commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()
        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('about'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
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


# STATIC PAGES

# About
@app.route('/about')
def about():
    return render_template('about.html')


# LIST OF RUs
class rudatasourceForm(Form):
    dbshortcode = StringField('DBShortCode', [validators.Length(min=1, max=10)])
    agree       = BooleanField('I agree.', )

# Dashboard of RU
@app.route('/ru_datasource',methods=['GET', 'POST'])
@is_logged_in
def ru_datasource():
    form = rudatasourceForm(request.form)
    # Create cursor
    cur = mysql.connection.cursor()

    # Get status list of RU
    # result=cur.execute("SELECT * FROM ru_registry where userid=%s ", (session['username']) )
    # cur.execute("SELECT * FROM ru_registry where userid='hibellm' ")
    # ru_status = cur.fetchall()

    result = cur.execute("select * from (SELECT id,dbshortcode,pdfcode,create_date FROM myflaskapp.datasourcelist) as a left join (SELECT * FROM myflaskapp.ru_registry where userid='hibellm') as b on a.dbshortcode=b.dbshortcode;")


    # Get datasourcelist
    # result = cur.execute("SELECT id,dbshortcode,pdfcode,create_date FROM datasourcelist")
    datasource = cur.fetchall()

    if result > 0:
        return render_template('ru_datasource.html', datasource=datasource,form=form)
    else:
        msg = 'No R&amp;U Found...strange'
        return render_template('ru_datasource.html', msg=msg ,form=form)
    # Close connection
    cur.close()


# Log a Request for access
@app.route('/request_access/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def request_access(id):
    form = rudatasourceForm(request.form)
    if request.method == 'POST' and form.validate():
        dbshortcode = form.dbshortcode.data
        agree       = form.agree.data
        dttime      = datetime.now()

    # Check if agree ticked
    if agree == 1:
        # Create Cursor
        cur = mysql.connection.cursor()
        # Execute
        cur.execute("INSERT INTO ru_registry(userid,dbshortcode,requestdate,request) VALUES(%s,%s,%s,%s)",(session['username'],dbshortcode,dttime,agree))
        # Commit to DB
        mysql.connection.commit()
        #Close connection
        cur.close()
        flash('DataSource ' + dbshortcode +' Access requested', 'success')
        return redirect(url_for('vendors'))
    else:
        flash('You have not ticked the "Agree". ' + dbshortcode +' Access not requested', 'danger')
        return redirect(url_for('vendors'))

    return render_template('add_datasource.html', form=form)


# Vendors
# @app.route('/vendors')
# def vendors():
#     # Create cursor
#     cur = mysql.connection.cursor()
#     # Get vendors
#     result = cur.execute("SELECT * FROM vendors")
#     vendors = cur.fetchall()
#
#     if result > 0:
#         return render_template('vendors.html', vendors=vendors)
#     else:
#         msg = 'No Vendors Found'
#         return render_template('vendors.html', msg=msg)
#     # Close connection
#     cur.close()
#
# #Single Vendor
# @app.route('/vendor/<string:id>/')
# def vendor(id):
#     # Create cursor
#     cur = mysql.connection.cursor()
#     # Get vendor
#     result = cur.execute("SELECT * FROM accessrole WHERE id = %s", [id])
#     vendor = cur.fetchone()
#     return render_template('vendor.html', vendor=vendor)


# Register Form Class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')






# Vendor Form Class
class VendorForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])


# Delete datasource
# @app.route('/delete_datasource/<string:id>', methods=['POST'])
# @is_logged_in
# def delete_datasource(id):
#     # Create cursor
#     cur = mysql.connection.cursor()
#     # Execute
#     cur.execute("DELETE FROM datasources WHERE id = %s", [id])
#     # Commit to DB
#     mysql.connection.commit()
#     #Close connection
#     cur.close()
#     flash('DataSource Deleted', 'success')
#     return redirect(url_for('dashboardd'))

# MY RU BITS
# RU Data source List
# rudatasource Form Class


# @app.route('/ru_datasource', methods=['GET', 'POST'])
# @is_logged_in
# def ru_datasource():
# ###
#     # Create cursor
#     cur = mysql.connection.cursor()
#
#     # Get vendor by id
#     result = cur.execute("SELECT * FROM vendors")
#     vendor = cur.fetchall()
#     cur.close()
# ###
#     form = rudatasourceForm(request.form)
#     if request.method == 'POST' and form.validate():
#         dbshortcode = form.dbshortcode.data
#         agree       = form.agree.data
#
#         # Create Cursor
#         cur = mysql.connection.cursor()
#         # Execute
#         cur.execute("INSERT INTO ru_registry(dbshortcode, author, agree) VALUES(%s, %s, %s)",(dbshortcode, session['username'], agree))
#         # Commit to DB
#         mysql.connection.commit()
#         # Close connection
#         cur.close()
#         flash('DataSource ' + dbshortcode +' Access Request Created', 'success')
#         return redirect(url_for('ru_datasource'))
#
#     return render_template('ru_datasource.html', form=form)


if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
