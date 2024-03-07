from flask import Flask, render_template, request, redirect, url_for,g, send_from_directory
import sqlite3
import os
from werkzeug.utils import secure_filename
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from Crypto.Cipher import DES3
import tkinter.messagebox as tkMessageBox
import subprocess


app = Flask(__name__)
app.secret_key = 'your_secret_key'
def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        salt=salt,
        length=32,
        backend=default_backend()
    )
    return kdf.derive(password.encode('utf-8'))

# Triple DES encryption function
def encrypt_text(text, key):
    cipher = Cipher(algorithms.TripleDES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    padded_text = text.ljust(16)  # Pad the text to be a multiple of the block size (8 bytes)
    ciphertext = encryptor.update(padded_text.encode('utf-8')) + encryptor.finalize()
    return ciphertext
# Function to create a connection to the SQLite database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect("master.db")
    return db

# Function to create tables in the database (execute only once)
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
@app.route('/')
def login():
    return render_template('login.html', error=None)

@app.route('/login', methods=['GET', 'POST'])
def login_post():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()

        if user:
            # Authentication successful
            return redirect(url_for('home'))
        else:
            # Authentication failed
            return render_template('login.html', error='Invalid credentials')

    return redirect(url_for('login'))

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/file')
def file():
    return render_template('file.html')
@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Perform signup logic and insert data into the database
        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        db.commit()

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    user_input = None
    encrypted_text = None

    return render_template('home.html', user_input=user_input, encrypted_text=encrypted_text)
@app.route('/words')
def words():
    subprocess.call(["python", "tdesEnc.py"])
    return render_template('home.html')
@app.route('/wordsde')
def wordsde():
    subprocess.call(["python", "tdesDecr.py"])
    return render_template('home.html')
@app.route('/filed')
def filed():
    # subprocess.call(["python", "fileotpDownl.py"])
    conn = sqlite3.connect('master.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM encrypted_files')
    db = cursor.fetchall()
    conn.close()
    return render_template('home.html', db = db)
    
DATABASE_FILE = 'master.db'

def pad(data):
    pad_length = 8 - (len(data) % 8)
    return data + bytes([pad_length] * pad_length)

def unpad(data):
    pad_length = data[-1]
    return data[:-pad_length]

def encrypt_data(data, key):
    cipher = DES3.new(key, DES3.MODE_ECB)
    padded_data = pad(data)
    encrypted_data = cipher.encrypt(padded_data)
    return encrypted_data

def store_encrypted_data_in_database(data, key):
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS encrypted_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data BLOB
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS encrypted_filesN (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data BLOB
        )
    ''')

    encrypted_data = encrypt_data(data, key)
    cursor.execute('INSERT INTO encrypted_files (data) VALUES (?)', (encrypted_data,))
    cursor.execute('INSERT INTO encrypted_filesN (data) VALUES (?)', (data,))

    connection.commit()
    connection.close()

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'fileInput' not in request.files:
            return render_template('file.html', message='No file part')

        file = request.files['fileInput']

        if file.filename == '':
            return render_template('file.html', message='No selected file')

        key = b'!\x83s\x14\xd3\xbbR\xb5\x08\xc52h4lA\x0euie\x818%\xa19'
        store_encrypted_data_in_database(file.read(), key)

        return render_template('file.html', message=tkMessageBox.showinfo("info",'File Success...',icon="info"))
        

    return render_template('/home.html', message='')

if __name__ == '__main__':
    app.run(debug=True)

