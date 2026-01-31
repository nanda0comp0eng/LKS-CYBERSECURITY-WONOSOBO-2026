import uuid
from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

users = {}
notes = []

# Dummy notes
for i in range(6):
    notes.append({
        'id': str(uuid.uuid4())[:8],
        'content': f"Dummy note {i+1}"
    })

def get_user_notes(username):
    # Only show dummy notes for non-admins
    return notes[:6]

@app.route('/')
def index():
    if 'username' in session:
        if session.get('isAdmin'):
            user_notes = [n for n in notes if n.get('owner') == session['username']] + notes[:6]
        else:
            user_notes = get_user_notes(session['username'])
    else:
        user_notes = notes[:6]
    return render_template('index.html', notes=user_notes)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            session['isAdmin'] = user['isAdmin']
            return redirect(url_for('index'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Mass assignment: isAdmin is accepted if present in POST, but not shown in form
        isAdmin = request.form.get('isAdmin', 'false')
        if username in users:
            return render_template('register.html', error='Username already exists')
        users[username] = {
            'password': generate_password_hash(password),
            'isAdmin': isAdmin.lower() == 'true'
        }
        session['username'] = username
        session['isAdmin'] = isAdmin.lower() == 'true'
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/create', methods=['GET', 'POST'])
def create():
    if not session.get('isAdmin'):
        return redirect(url_for('index'))
    if request.method == 'POST':
        content = request.form['content']
        # SSTI vulnerability here
        note = {
            'id': str(uuid.uuid4())[:8],
            'content': render_template_string(content),
            'owner': session['username']
        }
        notes.append(note)
        return redirect(url_for('index'))
    return render_template('create.html')

# SSTI vulnerable function
from flask import render_template_string

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
