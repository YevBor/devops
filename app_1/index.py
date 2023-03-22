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

def create_access_log_table():
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
    connection.commit()
    cursor.close()
    connection.close()

create_access_log_table()

global_counter = 0

@app.route('/')
def index():
    global global_counter
    global_counter += 1

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
    global global_counter
    return str(global_counter)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
