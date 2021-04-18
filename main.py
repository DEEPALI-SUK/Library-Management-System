from flask import Flask, render_template, request, redirect, url_for, session
import bcrypt
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os, uuid
from werkzeug.utils import secure_filename
from datetime import date, timedelta

app = Flask(__name__)

app.secret_key = '\x7f\xb0D\xfd}(\x1aP\xedt\xa5r^\xda\xa7tf\x1f\xf2V\x93\xf2n\x96'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'lms'

mysql = MySQL(app)

@app.route("/", methods=['GET', 'POST'])
def home():
    if 'loggedin' in session:
        return render_template('index.html', username=session['username'], email=session['email1'])
    else:
        return render_template('index.html', username="", email="")

@app.route("/update_profile/", methods=['GET', 'POST'])
def update_profile():
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST':
            name = request.form['name']
            password = request.form['password']
            email = request.form['email']
            address = request.form['address']
            cpassword = request.form['cpassword']
            if len(name) > 0 and len(password) > 0 and len(email) > 0 and len(address) > 0 and len(cpassword) > 0:
                if (email[:3] == 'lib' and email[-11:] == "@iiti.ac.in"):
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('SELECT * FROM librarian WHERE email = % s', (email,))
                    account = cursor.fetchone()
                    if account and account['email']!=session['email1']:
                        msg = 'Account already exists with this email!'
                    elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                        msg = 'Invalid email address !'
                    elif not name or not password or not email or not address or not cpassword or not address:
                        msg = 'Please fill out the form !'
                    elif cpassword != password:
                        msg = 'Confirm password does not match with password !'
                    else:
                        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                        cursor.execute('update librarian set lib_password=%s where L_Id=%s',(hashed,[session['id'], ]))
                        if session['email1']!=email:
                            session['email1']=email
                            cursor.execute('update librarian set email=%s where L_Id=%s',(email,[session['id'], ]))
                        if session['username']!=name:
                            session['username']=name
                            cursor.execute('update librarian set lib_name=%s where L_Id=%s', (name,[session['id'], ]))
                        if session['address']!=address:
                            session['address']=address
                            cursor.execute('update librarian set address=%s where L_Id=%s', (address,[session['id'], ]))
                        mysql.connection.commit()
                        cursor.close()
                        msg = 'Your profile has been successfully updated !'
                elif (email[-11:] == "@iiti.ac.in"):
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('SELECT * FROM lib_member WHERE email = % s', (email,))
                    account = cursor.fetchone()
                    if account and account['email']!=session['email1']:
                        msg = 'Account already exists with this email!'
                    elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                        msg = 'Invalid email address !'
                    elif not name or not password or not email or not address or not cpassword or not address:
                        msg = 'Please fill out the form !'
                    elif cpassword != password:
                        msg = 'Confirm password does not match with password !'
                    else:
                        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                        cursor.execute('update lib_member set member_password=%s where M_Id=%s', (hashed,[session['id'], ]))
                        if session['email1'] != email:
                            session['email1'] = email
                            cursor.execute('update lib_member set email=%s where M_Id=%s', (email,[session['id'], ]))
                        if session['username'] != name:
                            session['username'] = name
                            cursor.execute('update lib_member set member_name=%s where M_Id=%s', (name,[session['id'], ]))
                        if session['address'] != address:
                            session['address'] = address
                            cursor.execute('update lib_member set address=%s where M_Id=%s', (address,[session['id'], ]))
                        mysql.connection.commit()
                        cursor.close()
                        msg = 'Your profile has been successfully updated !'
                else:
                    msg = 'Invalid email address, not a member of institute !'
            else:
                msg = 'Please fill out the form !'
        return render_template('update_profile.html', username=session['username'],msg=msg,email=session['email1'],address=session['address'])
    else:
        return redirect(url_for('login'))

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
                    return redirect(url_for('lib_dashboard'))
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
                    return redirect(url_for('registeredusers'))
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
            if (email[:3] == 'lib' and email[-11:]=="@iiti.ac.in"):
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
            elif (email[-11:]=="@iiti.ac.in"):
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
                msg = 'Invalid email address, not a member of institute !'
        else:
            msg = 'Please fill out the form !'

    return render_template('register.html', msg=msg)


@app.route("/lib_dashboard/")
def lib_dashboard():
    if 'loggedin' in session:
        return render_template('lib_dashboard.html', username='librarian', email=session['email1'])
    return redirect(url_for('login'))


@app.route("/remove_book/", methods=['GET', 'POST'])
def remove_book():
    print('1')
    msg = ''
    if request.method == 'POST':
        print('2')
        isbn = request.form['isbn']
        count = request.form['count']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select shelf_Id,count from book where ISBN = %s', (isbn,))
        a = cursor.fetchone()
        print('3')
        print(a)
        cursor.execute('select capacity from shelf where shelf_Id = %s', (a['shelf_Id'],))
        c = cursor.fetchone()
        if int(count) <= int(a['count']):
                if int(a['count']-int(count))==0:
                    cursor.execute('update shelf set shelf_status = %s where shelf_Id = %s',
                                    ('available', a['shelf_Id'],))
                    cursor.execute('delete from book where ISBN = %s', (isbn), )
                cursor.execute('update shelf set capacity = %s where shelf_Id = %s', (int(c['capacity'])+int(count),a['shelf_Id'], ))
                cursor.execute('update book set count = %s where ISBN = %s', (int(a['count']) - int(count),isbn, ))

        else:
                msg = 'Cannot remove books .'

        print('hiiiiiii')
        mysql.connection.commit()
        cursor.close()

    if 'loggedin' in session:
        email = session['email1']
        if email[:3] == 'lib':
            return render_template('remove_book.html', username=session['username'], msg=msg, email=session['email1'])
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@app.route("/registeredusers/")
def registeredusers():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        resultValue = cur.execute("SELECT * FROM lib_member")
        if resultValue > 0:
            userDetails = cur.fetchall()
            cur.execute('select M_Id2 from follower_following where M_Id1= %s',([session['id']],))
            list=cur.fetchall()
            l=[]
            for i in list:
                l.append(i[0])

            mysql.connection.commit()
            cur.close()
            return render_template('registeredusers.html', userDetails=userDetails, l =l, username=session['username'],
                                   email=session['email1'])



@app.route("/add_book/", methods=['GET', 'POST'])
def add_book():
    print('1')
    msg = ''
    if request.method == 'POST':
        print('2')
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        year = request.form['year']
        count = request.form['count']
        category = request.form['category']
        file = request.files['file']
        filename = secure_filename(file.filename)
        extension = os.path.splitext(filename)
        allowed_extensions = {'.jpg', '.png', '.jpeg'}
        if extension[1] in allowed_extensions:
            f_name = str(uuid.uuid4()) + str(extension[1])
            app.config['UPLOAD_FOLDER'] = 'static/Uploads'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name))
            cursor1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor1.execute('select shelf_Id,count from book where ISBN = %s', (isbn,))
            a = cursor1.fetchone()
            if a:
                print('3')
                print(a)
                cursor1.execute('select capacity from shelf where shelf_Id = %s', (a['shelf_Id'],))
                c = cursor1.fetchone()
                if int(count) <= 75-int(a['count']):
                    cursor1.execute('update shelf set capacity = %s where shelf_Id = %s', (int(c['capacity'])-int(count),a['shelf_Id'], ))
                    cursor1.execute('update book set count = %s where ISBN = %s', (int(a['count']) + int(count),isbn, ))
                    if int(count)==75-int(a['count']):
                        cursor1.execute('update shelf set shelf_status = %s where shelf_Id = %s',
                                    ('no space', a['shelf_Id'],))
                else:
                    msg = 'Cannot add books overflow.'
            else:
                print('poppppiiiii')
                cursor1.execute('select shelf_Id from shelf where capacity = %s', (75,))
                s1 = cursor1.fetchone()
                print(s1)
                if int(count) <= 75:
                    print('4')
                    cursor1.execute('INSERT INTO book VALUES (%s, % s, % s, % s,% s,% s,% s,%s,% s)',
                                (isbn, title, author, year, s1['shelf_Id'], count,0,category,f_name))
                    cursor1.execute('update shelf set capacity = %s where shelf_Id = %s', (75-int(count),s1['shelf_Id'],))
                    if int(count)==75:
                        cursor1.execute('update shelf set shelf_status = %s where shelf_Id = %s',
                                    ('no space', s1['shelf_Id'],))

                else:
                    msg = 'Cannot add books overflow.'
            print('hiiiiiii')
            mysql.connection.commit()
            cursor1.close()
        else:
            msg = 'Upload image in jpg/png/jpeg format only!'
    if 'loggedin' in session:
        email = session['email1']
        if email[:3] == 'lib':
            return render_template('add_book.html', username=session['username'], msg=msg, email=session['email1'])
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@app.route("/books/", methods=['GET', 'POST'])
def books():
    msg = ''
    cursor1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor1.execute('select * from book ')
    details = cursor1.fetchall()
    mysql.connection.commit()
    cursor1.close()
    if 'loggedin' in session:
        return render_template('books.html', username=session['username'], msg=msg, detail=details,
                               email=session['email1'])
    else:
        return render_template('books.html', username="", msg=msg, detail=details, email="")

@app.route('/follow/<string:id>', methods=['GET', 'POST'])
def follow(id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        print(id)
        cur.execute('insert into follower_following values (%s, %s)', (session['id'], id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('registeredusers'))
    else:
        return redirect(url_for('login'))

@app.route('/unfollow/<string:id>', methods=['GET', 'POST'])
def unfollow(id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute('delete from follower_following where M_Id2= %s', ( id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('registeredusers'))

    else:
        return redirect(url_for('login'))

@app.route('/borrow_book/<string:id>', methods=['GET', 'POST'])
def borrow_book(id):
    msg=''
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select count(*) from borrow where M_Id=%s',[session['id'], ])
        c=cursor.fetchone()
        email=session['email1']
        if(email[:3]!='lib'):
            if (email[:7]!='faculty'):
              if(c['count(*)']>=3):
                msg='Oops!! you have already issued 3 books. You cannot issue more than 10 books.'
              else:
                cursor.execute('select * from borrow where M_Id=%s and ISBN=%s',([session['id'], ],[id, ]))
                flag=cursor.fetchone()
                if flag:
                    msg='Oops!! you can issue a particular book only one time until you return the same!'
                else:
                    cursor.execute('insert into borrow values (%s,%s)',(session['id'],id))
                    start_date=date.today()
                    end_date= start_date+timedelta(15)
                    cursor.execute('insert into book_status values (%s,%s,%s,%s)',(session['id'],id,start_date,end_date))
                    cursor.execute('update book set borrow_count =borrow_count+1 where ISBN=%s',[id, ])
                    cursor.execute('update shelf set capacity =capacity+1 where shelf_Id=(select shelf_Id from book where ISBN=%s)', [id, ])
                    msg='Book got issued succesfully! :)'
            else:
             cursor.execute('select * from borrow where M_Id=%s and ISBN=%s', ([session['id'], ], [id, ]))
             flag = cursor.fetchone()
             if flag:
                msg = 'Oops!! you can issue a particular book only one time until you return the same!'
             else:
                cursor.execute('INSERT INTO borrow values (%s,%s)', (session['id'], id))
                start_date = date.today()
                end_date = start_date + timedelta(15)
                cursor.execute('insert into book_status values (%s,%s,%s,%s)',
                               (session['id'], id, start_date, end_date))
                cursor.execute('update book set borrow_count =borrow_count+1 where ISBN=%s', [id, ])
                cursor.execute(
                    'update shelf set capacity =capacity+1 where shelf_Id=(select shelf_Id from book where ISBN=%s)',
                    [id, ])
                msg = 'Book got issued succesfully! :)'
        cursor.execute('select * from book ')
        details = cursor.fetchall()
        mysql.connection.commit()
        return render_template('books.html', username=session['username'],msg=msg,detail=details,email=email)
    else:
        return redirect(url_for('login'))

app.run(debug=True)