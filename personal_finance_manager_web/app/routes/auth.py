from flask import Blueprint, render_template, request, redirect, session, flash
from ..db import connect_db


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    return render_template('login.html')

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT user_id FROM users WHERE Username = %s AND Password = %s", (username, password))
        user = cursor.fetchone()
    except Exception as e:
        print(f"Login error: {e}")
        user = None
    finally:
        conn.close()

    if user:
        session['user_id'] = user[0]
        return redirect('/dashboard')
    else:
        flash("Invalid username or password", "error")
        return redirect('/')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = {key: request.form[key] for key in request.form}
        if not all(data.values()):
            flash("Fill in all fields", "error")
            return redirect('/register')

        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT user_id FROM users WHERE Username = %s", (data['username'],))
            if cursor.fetchone():
                flash("Username already exists", "error")
                return redirect('/register')

            cursor.execute("""
                INSERT INTO users (first_Name, last_Name, Username, Password, birthday, Occupation, Location)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                data['first_name'],
                data['last_name'],
                data['username'],
                data['password'],
                data['birthday'],
                data['occupation'],
                data['location']
            ))
            conn.commit()
            flash("Account created successfully!", "success")
            return redirect('/')
        except Exception as e:
            print(f"Registration error: {e}")
            flash("Error during registration", "error")
            return redirect('/register')
        finally:
            conn.close()

    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')
