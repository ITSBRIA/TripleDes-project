import sqlite3
def retrieve_and_save_encrypted_data_from_database(database_file, table_name, output_file):
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    cursor.execute(f'SELECT data FROM {table_name} ORDER BY id DESC LIMIT 1')
    row = cursor.fetchone()
    if row:
        encrypted_data = row[0]
        with open(output_file, 'wb') as f:
            f.write(encrypted_data)
    connection.close()
database_file = 'master.db'
table_name = 'encrypted_data_table'
downloaded_file = 'downloaded_encrypted_file.bin'
retrieve_and_save_encrypted_data_from_database(database_file, table_name, downloaded_file)
