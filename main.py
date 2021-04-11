import sqlite3
from flask import render_template, flash, Flask, url_for, request, redirect, get_flashed_messages

app = Flask(__name__, template_folder="template")
app.secret_key='abc'

connection = ''
try:
    connection = sqlite3.connect('user_data.db')
    connection.execute('create table user(user_name TEXT NOT NULL, user_email TEXT UNIQUE NOT NULL PRIMARY KEY, user_pass TEXT NOT NULL)')
except Exception as e:
    print(e)
finally:
    connection.close()

@app.route('/')
def home_view(*args):
    return render_template('home.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['pass']
        C_password = request.form['c_pass']
        user_email = request.form['user_email']

        if password == C_password:
            if len(password) >=8:
                try:
                    with sqlite3.connect('user_data.db') as db:
                        cur = db.cursor()
                        cur.execute('insert into user(user_name, user_email, user_pass) values(?,?,?)', (user_name,user_email,password))
                        db.commit()

                    return redirect(url_for('login_view'))

                except Exception as e:
                    db.rollback()
                    flash('*Try again later')
                    print(e)
                    return redirect(url_for('register'))

                finally:
                    db.close()

            else:
                flash('*password should be at least of 8 characters')
                return redirect(url_for('register'))
        
        else:
            flash('*password does not match')
            return redirect(url_for('register'))

    else:
        return render_template('registration.html')

@app.route('/login', methods=['POST', 'GET'])
def login_view():
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']

        try:
            with sqlite3.connect('user_data.db') as db:
                cur = db.cursor()
                cur.execute('select * from user where user_name=(?) and user_pass=(?)',(user_name, password))
                rows = cur.fetchall()
                for row in rows:
                    if user_name in row and password in row:
                        flash(f'WELCOME!!! {user_name.upper()}')
                        return redirect(url_for('home_view'))
                
        except Exception as e:
            print(e)
            flash('*Re-Try')
            return redirect(url_for('login_view'))

        finally:
            db.close()

        
    else:
        return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)