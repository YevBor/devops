from flask import Flask, request, make_response
import mysql.connector
import socket
from datetime import datetime, timedelta

app = Flask(__name__)

# Replace with your MySQL connection details
db_config = {
    'user': 'test',
    'password': 'test',
    'host': 'db',
    'database': 'mydb',
}

def create_tables():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS access_log (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date_time DATETIME,
            client_ip VARCHAR(255),
            server_internal_ip VARCHAR(255)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS global_counter (
            id INT AUTO_INCREMENT PRIMARY KEY,
            count INT NOT NULL
        )
    ''')
    
    cursor.execute("INSERT IGNORE INTO global_counter (id, count) VALUES (1, 0)")
    
    connection.commit()
    cursor.close()
    connection.close()

create_tables()

def increment_global_counter():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("UPDATE global_counter SET count = count + 1 WHERE id = 1")
    connection.commit()
    cursor.close()
    connection.close()

def get_global_counter():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT count FROM global_counter WHERE id = 1")
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result[0] if result else 0

@app.route('/')
def index():
    increment_global_counter()

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    date_time = datetime.now()
    client_ip = request.remote_addr
    server_internal_ip = socket.gethostbyname(socket.gethostname())

    cursor.execute('''
        INSERT INTO access_log (date_time, client_ip, server_internal_ip)
        VALUES (%s, %s, %s)
    ''', (date_time, client_ip, server_internal_ip))

    connection.commit()
    cursor.close()
    connection.close()

    response = make_response(server_internal_ip)
    expires = datetime.now()
    expires = expires + timedelta(minutes=5)
    response.set_cookie('internal_ip', server_internal_ip, expires=expires)

    return response

@app.route('/showcount')
def showcount():
    global_counter = get_global_counter()
    return str(global_counter)

if __name__ == '__main__':
    app.run(debug=True)
