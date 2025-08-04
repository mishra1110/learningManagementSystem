from flask import Flask, request
from flask import render_template
from flask import redirect, url_for
from flask import session
import mysql.connector
import _mysql_connector
app = Flask(__name__)
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='lms'
    )
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/login',methods=['POST','GET'])
def login():
    return render_template('login.html')

@app.route('/register',methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        
        lFname=request.form['lFname']
        lLname=request.form['lLname']
        lEmail=request.form['lEmail']
        lPassword=request.form['lPassword']
        conn = get_db_connection()
        cursor= conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM learner WHERE lEmail = %s", (lEmail,))
        user = cursor.fetchone()
        if user:
            return render_template('register.html', error="Email already exists")
        cursor = conn.cursor(dictionary=True)
        cursor.execute("insert into learner(lFname,lLname,lEmail,lpassword) values(%s,%s,%s,%s)", (lFname,lLname,lEmail,lPassword))   
        conn.commit()
        cursor.close()
        conn.close()

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
