from flask import Flask, request
import sqlite3
import sys
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "mydatabase.db")

def create_table():
    try:

        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS uuids (username TEXT, uuid TEXT, status TEXT)')  # Add a status column to your table
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        sys.exit(1)

@app.route('/')
def home():
    return "Home"

@app.route('/send_uuid', methods=['POST'])
def receive_uuid():
    try:
        uuid = request.form.get('uuid')
        username = request.form.get('username')
        status = 'pending'  # Set the status to 'pending'
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('INSERT INTO uuids VALUES (?, ?, ?)', (username, uuid, status))  # Insert the username, UUID, and status into the database
        conn.commit()
        conn.close()
        return "Pending approval", 200
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return "Error occurred", 500

@app.route('/check_uuid', methods=['GET'])
def check_uuid():
    uuid = request.args.get('uuid')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM uuids WHERE uuid=? AND status=?', (uuid, 'active'))  # Check if the UUID exists in the database and is active
    rows = c.fetchall()
    conn.close()
    if len(rows) > 0:
        return "UUID exists", 200
    else:
        return "UUID does not exist or is not active", 404

@app.route('/api/check_uuid', methods=['GET'])
def api_check_uuid():
    uuid = request.args.get('uuid')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM uuids WHERE uuid=? AND status=?', (uuid, 'active'))  # Check if the UUID exists in the database and is active
    rows = c.fetchall()
    conn.close()
    if len(rows) > 0:
        return {"exists": True}, 200
    else:
        return {"exists": False}, 404

@app.route('/approve_user', methods=['POST'])
def approve_user():
    username = request.form.get('username')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('UPDATE uuids SET status = ? WHERE username = ?', ('active', username))  # Set the status to 'active' for the specified user
    conn.commit()
    conn.close()
    return "User approved", 200

@app.route('/delete_user', methods=['POST'])
def delete_user():
    username = request.form.get('username')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('DELETE FROM uuids WHERE username = ?', (username,))  # Delete the user with the specified username
    conn.commit()
    conn.close()
    return "User deleted", 200

create_table()


