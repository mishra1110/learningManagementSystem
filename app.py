from flask import Flask, request, render_template, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "lecturo_secret_key"

# ------------------- DATABASE CONNECTION -------------------
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='lms'
    )

# ------------------- HOME PAGE -------------------
@app.route('/')
def index():
    return render_template('index.html')

# ------------------- LOGIN ROUTE -------------------
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        lEmail = request.form['email']
        lPassword = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM learner WHERE lEmail = %s AND lPassword = %s", (lEmail, lPassword))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['email'] = user['lEmail']
            render_template("dashboard.html", email=user['lEmail'])
        else:
            return render_template('login.html', error="⚠️ Invalid Email or Password")

    return render_template('login.html')

# ------------------- REGISTER ROUTE -------------------
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        lFname = request.form['lFname']
        lLname = request.form['lLname']
        lEmail = request.form['lEmail']
        lPassword = request.form['lPassword']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM learner WHERE lEmail = %s", (lEmail,))
        user = cursor.fetchone()

        if user:
            cursor.close()
            conn.close()
            return render_template('register.html', error="⚠️ Email already exists. Try logging in.")

        cursor.execute("INSERT INTO learner (lFname, lLname, lEmail, lPassword) VALUES (%s, %s, %s, %s)",
                       (lFname, lLname, lEmail, lPassword))
        conn.commit()
        cursor.close()
        conn.close()

        return render_template('login.html', success="✅ Registration successful! Please log in.")
    else:
        return render_template('register.html')

# ------------------- DASHBOARD -------------------
@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', email=session['email'])

# ------------------- UPLOAD -------------------
@app.route('/upload')
def upload():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template('upload.html')

# ------------------- LOGOUT -------------------
@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

# ------------------- MAIN -------------------
if __name__ == '__main__':
    app.run(debug=True)
