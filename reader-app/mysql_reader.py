from flask import Flask, jsonify
import mysql.connector
import time
import random
import os
from datetime import datetime
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
import threading

app = Flask(__name__)
# Database connection settings
# Database connection settings
QUERY_RESPONSE_TIME = Gauge('mysql_query_response_time_miliseconds', 'Time taken to execute SQL read query')

MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql-service")  # Default to "mysql-service"
MYSQL_USER = os.getenv("MYSQL_USER", "default_user")  # Default if not set
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "default_password")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "test_db")

# Function to establish a connection with retry mechanism
def get_db_connection():
    while True:
        try:
            conn = mysql.connector.connect(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_DATABASE
            )
            print("Connected to MySQL successfully!")
            return conn
        except mysql.connector.Error as err:
            print(f"Database connection failed: {err}. Retrying in 5 seconds...")
            time.sleep(5)

def check_database_connection():
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        conn.close()
        return True
    except Exception as e:
        print(f"Database connection failed: {e}", flush=True)
        return False

def count_rows():
    conn = get_db_connection()
    cursor = conn.cursor()
    start_time = time.time()
    cursor.execute("SELECT COUNT(*) FROM sample_data;")
    row_count = cursor.fetchone()[0]
    end_time = time.time()
    response_time = (end_time - start_time) * 1000
    QUERY_RESPONSE_TIME.set(response_time)
    cursor.close()
    conn.close()
    return row_count, response_time
    
def log_row_count():
    """Logs the total row count to stdout every second as per the requirement while keeping http endpoint."""
    while True:
        row_count, response_time = count_rows()
        print(f"Number of rows in sample_data table: {row_count}, And query time is: {response_time:.2f} ms")
        time.sleep(1)
        
@app.route('/rows', methods=['GET'])
def get_row_count():
    """API endpoint to fetch row count"""
    row_count = count_rows()
    return jsonify({"total_rows, query time": row_count})

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}
    
@app.route("/health", methods=["GET"])
def health_check():
    if check_database_connection():
        return jsonify({"status": "ok"}), 200  # App + DB Ready
    else:
        return jsonify({"status": "not ready"}), 503  # Service Unavailable
    
if __name__ == "__main__":
    thread = threading.Thread(target=log_row_count, daemon=True)
    thread.start()

    # Run Flask application
    app.run(host="0.0.0.0", port=5000)
