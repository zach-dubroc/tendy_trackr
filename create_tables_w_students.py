import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection details
DATABASE_URL = os.getenv("DATABASE_URL")

# Parse the DATABASE_URL to extract connection details
# Format: mysql://username:password@host:port/database

url = DATABASE_URL.split("//")[1]
username_password, host_port_db = url.split("@")
username, password = username_password.split(":")
host_port, database = host_port_db.split("/")
host, port = host_port.split(":")

# Connect to the database
connection = mysql.connector.connect(
    host=host,
    port=port,
    user=username,
    password=password,
    database=database
)

# Create a cursor object
cursor = connection.cursor()

# SQL commands to create tables
create_students_table = """
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fname VARCHAR(255),
    lname VARCHAR(255),
    absences INT,
    tardy INT,
    nocalls INT,
    currentStatus INT,
    datesMissed JSON
);
"""

create_users_table = """
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX (username),
    INDEX (email)
);
"""


# SQL commands to insert test students
insert_test_students = """
INSERT INTO students (fname, lname, absences, tardy, nocalls, currentStatus, datesMissed)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

# Test student data
students = [
    ("Zack", "Dubroc", 0, 0, 0, 1, '[]'),
    ("Margarito", "Valencia", 0, 0, 0, 1, '[]')
]

# Execute SQL commands
try:
    cursor.execute(create_students_table)
    cursor.execute(create_users_table)
    connection.commit()
    print("Tables created successfully")
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    # Close the cursor and connection
    print("nothing happened")
    cursor.close()
    connection.close()
