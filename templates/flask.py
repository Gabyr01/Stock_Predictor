# app.py

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_submit():
    username = request.form['username']
    password = request.form['password']
    
    if username == 'admin' and password == 'password':
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', message='Invalid username or password')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
