from flask import Flask, render_template, request, redirect, url_for, session
import bcrypt
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os, uuid

app = Flask(__name__)

app.secret_key = '\x7f\xb0D\xfd}(\x1aP\xedt\xa5r^\xda\xa7tf\x1f\xf2V\x93\xf2n\x96'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'lib_mang_system'

mysql = MySQL(app)

@app.route("/", methods=['GET', 'POST'])
def home():
    if 'loggedin' in session:
        return render_template('index.html', username=session['username'])
    else:
        return render_template('index.html', username="")

@app.route("/login/", methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if len(email) > 0 and len(password) > 0:
            if (email[:3]=='lib'):
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM librarian WHERE email = %s', (email,))
                account = cursor.fetchone()
                mysql.connection.commit()
                cursor.close()
                if account and bcrypt.checkpw(password.encode('utf-8'), account['lib_password'].encode('utf-8')):
                    session['loggedin'] = True
                    session['id'] = account['L_Id']
                    session['username'] = account['lib_name']
                    session['email1'] = account['email']
                    session['address'] = account['address']
                    return redirect(url_for('home'))
                else:
                  msg = 'Incorrect email/password!'
            else:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM lib_member WHERE email = %s', (email,))
                account = cursor.fetchone()
                mysql.connection.commit()
                cursor.close()
                if account and bcrypt.checkpw(password.encode('utf-8'), account['member_password'].encode('utf-8')):
                    session['loggedin'] = True
                    session['id'] = account['M_Id']
                    session['username'] = account['member_name']
                    session['email1'] = account['email']
                    session['address'] = account['address']
                    return redirect(url_for('home'))
                else:
                  msg = 'Incorrect email/password!'
        else:
            msg = ' Please fill the entries !'
    return render_template('login.html', msg=msg)

@app.route('/login/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('email1', None)
    session.pop('address', None)
    return redirect(url_for('login'))

@app.route("/register/", methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        address = request.form['address']
        cpassword = request.form['cpassword']
        if len(name) > 0 and len(password) > 0 and len(email) > 0 and len(address) > 0 and len(cpassword) > 0:
            if (email[:3] == 'lib'):
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM librarian WHERE email = % s', (email,))
                account = cursor.fetchone()
                if account:
                    msg = 'Account already exists with this email!'
                elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                    msg = 'Invalid email address !'
                elif not name or not password or not email or not address or not cpassword or not address:
                    msg = 'Please fill out the form !'
                elif cpassword != password:
                    msg = 'Confirm password does not match with password !'
                else:
                    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    cursor.execute('INSERT INTO librarian VALUES (NULL, % s, % s, % s,% s)',
                                   ( name, hashed, address,email,))
                    mysql.connection.commit()
                    cursor.close()
                    msg = 'You have successfully registered !'
            else:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM lib_member WHERE email = % s', (email,))
                account = cursor.fetchone()
                if account:
                    msg = 'Account already exists with this email!'
                elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                    msg = 'Invalid email address !'
                elif not name or not password or not email or not address or not cpassword or not address:
                    msg = 'Please fill out the form !'
                elif cpassword != password:
                    msg = 'Confirm password does not match with password !'
                else:
                    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    cursor.execute('INSERT INTO lib_member VALUES (NULL, % s, % s, % s,% s, %s)',
                                   (hashed, name, address, 0, email,))
                    mysql.connection.commit()
                    cursor.close()
                    msg = 'You have successfully registered !'
        else:
            msg = 'Please fill out the form !'

    return render_template('register.html', msg=msg)

app.run(debug=True)