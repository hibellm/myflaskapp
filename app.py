from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
#from data import Vendors
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, RadioField, validators
from passlib.hash import sha256_crypt
from functools import wraps

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
    result = cur.execute("SELECT * FROM vendors WHERE id = %s", [id])
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

# Dashboard
@app.route('/dashboardv')
@is_logged_in
def dashboardv():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get vendors
    result = cur.execute("SELECT * FROM vendors")
    vendors = cur.fetchall()

    if result > 0:
        return render_template('dashboardv.html', vendors=vendors)
    else:
        msg = 'No Vendors Found'
        return render_template('dashboardv.html', msg=msg)
    # Close connection
    cur.close()

# Dashboardd
@app.route('/dashboardd')
@is_logged_in
def dashboardd():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get datasources
    result = cur.execute("SELECT * FROM datasources")
    datasources = cur.fetchall()

    if result > 0:
        return render_template('dashboardd.html', datasources=datasources)
    else:
        msg = 'No datasources Found'
        return render_template('dashboardd.html', msg=msg)
    # Close connection
    cur.close()

# Vendor Form Class
class VendorForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])

# Add Vendor
@app.route('/add_vendor', methods=['GET', 'POST'])
@is_logged_in
def add_vendor():
    form = VendorForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        # Create Cursor
        cur = mysql.connection.cursor()
        # Execute
        cur.execute("INSERT INTO vendors(title, body, author) VALUES(%s, %s, %s)",(title, body, session['username']))
        # Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()
        flash('Vendor Created', 'success')
        return redirect(url_for('dashboardv'))

    return render_template('add_vendor.html', form=form)


# Edit Vendor
@app.route('/edit_vendor/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_vendor(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get vendor by id
    result = cur.execute("SELECT * FROM vendors WHERE id = %s", [id])
    vendor = cur.fetchone()
    cur.close()
    # Get form
    form = VendorForm(request.form)

    # Populate vendor form fields
    form.title.data = vendor['title']
    form.body.data = vendor['body']

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']

        # Create Cursor
        cur = mysql.connection.cursor()
        app.logger.info(title)
        # Execute
        cur.execute ("UPDATE vendors SET title=%s, body=%s WHERE id=%s",(title, body, id))
        # Commit to DB
        mysql.connection.commit()
        #Close connection
        cur.close()
        flash('Vendor Updated', 'success')
        return redirect(url_for('dashboardv'))

    return render_template('edit_vendor.html', form=form)


# Delete Vendor
@app.route('/delete_vendor/<string:id>', methods=['POST'])
@is_logged_in
def delete_vendor(id):
    # Create cursor
    cur = mysql.connection.cursor()
    # Execute
    cur.execute("DELETE FROM vendors WHERE id = %s", [id])
    # Commit to DB
    mysql.connection.commit()
    #Close connection
    cur.close()
    flash('Vendor Deleted', 'success')
    return redirect(url_for('dashboardv'))

########
# datasource Form Class
class datasourceForm(Form):
    dbshortcode = StringField('DBShortCode', [validators.Length(min=1, max=10)])
    description = TextAreaField('Description', [validators.Length(min=30)])
    hosting     = RadioField('Hosting', choices=[('EU', 'EU'), ('US', 'US')])
    link        = StringField('Link')

# Add datasource
@app.route('/add_datasource', methods=['GET', 'POST'])
@is_logged_in
def add_datasource():
    form = datasourceForm(request.form)
    if request.method == 'POST' and form.validate():
        dbshortcode = form.dbshortcode.data
        description = form.description.data
        hosting = form.hosting.data
        link = form.link.data

        # Create Cursor
        cur = mysql.connection.cursor()
        # Execute
        cur.execute("INSERT INTO datasources(dbshortcode, description, hosting, link, author) VALUES(%s, %s, %s, %s, %s)",(dbshortcode, description, hosting, link, session['username']))
        # Commit to DB
        mysql.connection.commit()
        #Close connection
        cur.close()
        flash('DataSource ' + dbshortcode +' Created', 'success')
        return redirect(url_for('dashboardd'))

    return render_template('add_datasource.html', form=form)


# Edit datasource
@app.route('/edit_datasource/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_datasource(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get datasource by id
    result = cur.execute("SELECT * FROM datasources WHERE id = %s", [id])
    datasource = cur.fetchone()
    cur.close()
    # Get form
    form = datasourceForm(request.form)

    # Populate datasource form fields
    form.dbshortcode.data = datasource['dbshortcode']
    form.description.data = datasource['description']
    form.hosting.data = datasource['hosting']
    form.link.data = datasource['link']

    if request.method == 'POST' and form.validate():
        dbshortcode = request.form['dbshortcode']
        description = request.form['description']
        hosting = request.form['hosting']
        link = request.form['link']

        # Create Cursor
        cur = mysql.connection.cursor()
        app.logger.info(dbshortcode)
        # Execute
        cur.execute ("UPDATE datasources SET dbshortcode=%s, description=%s, hosting=%s, link=%s WHERE id=%s",(dbshortcode, description, hosting, link, id))
        # Commit to DB
        mysql.connection.commit()
        #Close connection
        cur.close()
        flash('DataSource ' + dbshortcode + ' Updated', 'success')
        return redirect(url_for('dashboardd'))

    return render_template('edit_datasource.html', form=form)

# Delete datasource
@app.route('/delete_datasource/<string:id>', methods=['POST'])
@is_logged_in
def delete_datasource(id):
    # Create cursor
    cur = mysql.connection.cursor()
    # Execute
    cur.execute("DELETE FROM datasources WHERE id = %s", [id])
    # Commit to DB
    mysql.connection.commit()
    #Close connection
    cur.close()
    flash('DataSource Deleted', 'success')
    return redirect(url_for('dashboardd'))


if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
