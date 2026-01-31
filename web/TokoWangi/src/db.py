from flask import g
import pymysql
import os
import time

from pymysql.err import OperationalError

# Database config from env (for Docker/mariadb)
DB_HOST = os.environ.get('DB_HOST', 'mariadb')
DB_USER = os.environ.get('DB_USER', 'ctf')
DB_PASS = os.environ.get('DB_PASS', 'ctfpass')
DB_NAME = os.environ.get('DB_NAME', 'shop')

def get_db():
    if 'db' not in g:
        retries = int(os.environ.get('DB_RETRIES', '20'))
        delay = float(os.environ.get('DB_RETRY_DELAY', '1'))
        last_exc = None
        for attempt in range(1, retries + 1):
            try:
                g.db = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME, autocommit=True)
                return g.db
            except OperationalError as e:
                last_exc = e
                # brief log to stdout so docker logs show progress
                print(f"DB connection attempt {attempt}/{retries} failed: {e}")
                time.sleep(delay)
        # if we exhausted retries, raise the last exception
        raise last_exc
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    cur = db.cursor()
    # Create tables
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
      id INT AUTO_INCREMENT PRIMARY KEY,
      username VARCHAR(100) UNIQUE,
      password VARCHAR(100),
      balance INT DEFAULT 100
    ) ENGINE=InnoDB;
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS items (
      id INT AUTO_INCREMENT PRIMARY KEY,
      name VARCHAR(200),
      price INT
    ) ENGINE=InnoDB;
    ''')
    # Seed admin/user and items if empty
    cur.execute('SELECT COUNT(*) FROM users')
    row = cur.fetchone()
    if row is None or row[0] == 0:
        cur.execute("INSERT INTO users (username, password, balance) VALUES ('player','password', 100)")
        cur.execute("INSERT INTO users (username, password, balance) VALUES ('admin','adminpass', 1000)")

    cur.execute('SELECT COUNT(*) FROM items')
    row = cur.fetchone()
    if row is None or row[0] == 0:
        # Add FLAG item expensive and 20 dummy items
        cur.execute("INSERT INTO items (name, price) VALUES (%s, %s)", ('FLAG', 7777777))
        for i in range(1, 21):
            cur.execute("INSERT INTO items (name, price) VALUES (%s, %s)", (f'Perfume {i}', i*5 + 10))
