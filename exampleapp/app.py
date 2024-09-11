from flask import Flask, jsonify, render_template_string
import psycopg2
from psycopg2 import OperationalError
import os

app = Flask(__name__)

# Configuration for PostgreSQL connection
DB_HOST = "your_db_host"
DB_PORT = "your_db_port"
DB_NAME = "your_db_name"

# Read DB_USER and DB_PASSWORD from environment variables
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Function to connect to the PostgreSQL database
def connect_to_db():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return connection
    except OperationalError as e:
        print(f"Error: {e}")
        return None

# Index page with links to the API endpoints
@app.route('/')
def index():
    html_content = '''
    <h1>ExampleApp PostgreSQL API</h1>
    <ul>
        <li><a href="/status">Status Endpoint</a></li>
        <li><a href="/secret">Secret Endpoint</a></li>
    </ul>
    '''
    return render_template_string(html_content)

# Endpoint to check the status of the PostgreSQL connection
@app.route('/status', methods=['GET'])
def status():
    connection = connect_to_db()
    if connection:
        connection.close()
        return jsonify({"status": "success", "message": "Connected to the database successfully"}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to connect to the database"}), 500

# Endpoint to show the PostgreSQL username and password
@app.route('/secret', methods=['GET'])
def secret():
    return jsonify({
        "username": DB_USER,
        "password": DB_PASSWORD
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
