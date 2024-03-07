import sqlite3
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
def pad(data):
    pad_length = 8 - (len(data) % 8)
    return data + bytes([pad_length] * pad_length)
def unpad(data):
    pad_length = data[-1]
    return data[:-pad_length]

def encrypt_file(input_file, key):
    cipher = DES3.new(key, DES3.MODE_ECB)
    with open(input_file, 'rb') as f:
        plaintext = f.read()
        padded_plaintext = pad(plaintext)
        ciphertext = cipher.encrypt(padded_plaintext)
    return ciphertext
def decrypt_data(ciphertext, key):
    cipher = DES3.new(key, DES3.MODE_ECB)
    decrypted_data = cipher.decrypt(ciphertext)
    unpadded_data = unpad(decrypted_data)
    return unpadded_data

def store_encrypted_data_in_database(database_file, table_name, input_file, key):
    ciphertext = encrypt_file(input_file, key)
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data BLOB,file_extension text
        )
    ''')
    connection.close()
def retrieve_and_decrypt_data_from_database(database_file, table_name, output_file):
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    cursor.execute(f'SELECT data FROM {table_name} ORDER BY id DESC LIMIT 1')
    row = cursor.fetchone()
    if row:
        download_last_file_from_database()
        
    connection.close()
key =b'!\x83s\x14\xd3\xbbR\xb5\x08\xc52h4lA\x0euie\x818%\xa19'
input_file = decrypt_data
database_file = 'master.db'
table_name = 'encrypted_filesN'
decrypted_file = 'decrypted_file.pdf'
retrieve_and_decrypt_data_from_database(database_file, table_name,input_file)
import sqlite3

def download_last_file_from_database(output_filename):
    # Connect to the SQLite database (replace with your database connection code)
    connection = sqlite3.connect('master.db')
    cursor = connection.cursor()
    query = "SELECT data, file_extension FROM files ORDER BY id DESC LIMIT 1"
    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        file_data, file_extension = result

        full_filename = f"{output_filename}.{file_extension}"
        with open(full_filename, 'wb') as file:
            file.write(file_data)

        print(f"Last file downloaded and saved as: {full_filename}")
    else:
        print("No files found in the database.")

    connection.close()
download_last_file_from_database('downloaded_last_file')
