from flask import Flask, jsonify
import mysql.connector
import time
import random
import os
from datetime import datetime
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
import threading

app = Flask(__name__)

QUERY_RESPONSE_TIME = Gauge('mysql_query_response_time_miliseconds_writer', 'Time taken to execute SQL read query')
# Database connection settings
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

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sample_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            value INT,
            timestamp DATETIME
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    print("Table check/creation complete.")

def insert_sample_data():
    create_table()
    conn = get_db_connection()
    cursor = conn.cursor()

    while True:
        sample_value = random.randint(1, 100)
        timestamp = datetime.now()
        try:
            start_time = time.time()
            cursor.execute("INSERT INTO sample_data (value, timestamp) VALUES (%s, %s)", (sample_value, timestamp))
            conn.commit()
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            QUERY_RESPONSE_TIME.set(response_time)
            print(f"Inserted: {sample_value} at {timestamp} with time in {response_time}")
        except mysql.connector.Error as err:
            print(f"Error inserting data: {err}")
        
        time.sleep(1)  # Wait 1 second before inserting the next record

    cursor.close()
    conn.close()

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    thread = threading.Thread(target=insert_sample_data, daemon=True)
    thread.start()
    
    app.run(host="0.0.0.0", port=6000)