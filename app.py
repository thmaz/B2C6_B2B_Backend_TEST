from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
import mysql.connector
from mysql.connector import Error


app = Flask(__name__)
bcrypt = Bcrypt(app)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DATABASE'] = 'school_project'

def get_db_connection():
    connection = mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DATABASE']
    )
    return connection

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    wachtwoord = data['wachtwoord']

    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()

    if user and bcrypt.check_password_hash(user[3], wachtwoord):
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401

if __name__ == '__main__':
    app.run(debug=True)
