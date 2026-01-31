from flask import Flask, render_template, request, redirect, url_for, session
import os
from db import get_db, close_db, init_db

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev_secret')

@app.teardown_appcontext
def _close_db(e=None):
    close_db(e)

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('shop'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db = get_db()
        cur = db.cursor()
        cur.execute('SELECT id, password, balance FROM users WHERE username=%s', (username,))
        row = cur.fetchone()
        if row and row[1] == password:
            session['user'] = {'id': row[0], 'username': username}
            session['balance'] = row[2]
            return redirect(url_for('shop'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            return render_template('register.html', error='Username and password required')
        db = get_db()
        cur = db.cursor()
        try:
            cur.execute('INSERT INTO users (username, password, balance) VALUES (%s, %s, %s)', (username, password, 100))
            return redirect(url_for('login'))
        except Exception as e:
            return render_template('register.html', error='Username already taken')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/shop')
def shop():
    if 'user' not in session:
        return redirect(url_for('login'))
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT id, name, price FROM items')
    items = cur.fetchall()
    balance = session.get('balance', 0)
    return render_template('shop.html', items=items, balance=balance)

@app.route('/buy', methods=['POST'])
def buy():
    if 'user' not in session:
        return redirect(url_for('login'))
    item_id = request.form.get('item_id')
    client_price = request.form.get('price')
    try:
        price = int(client_price)
    except Exception:
        return 'Invalid price', 400

    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT balance FROM users WHERE id=%s', (session['user']['id'],))
    row = cur.fetchone()
    if not row:
        return 'User not found', 404
    balance = row[0]

    if price > balance:
        return 'Insufficient funds', 400

    cur.execute('UPDATE users SET balance = balance - %s WHERE id=%s', (price, session['user']['id']))
    session['balance'] = balance - price

    cur.execute('SELECT name FROM items WHERE id=%s', (item_id,))
    it = cur.fetchone()
    if it and it[0] == 'FLAG':
        flag = os.environ.get('CTF_FLAG', 'CTF{dummy_flag}')
        return render_template('flag.html', flag=flag)

    return redirect(url_for('shop'))

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(host='0.0.0.0', port=5000)
