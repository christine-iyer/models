from dotenv import load_dotenv
import os
import mysql.connector
import json

# Load environment variables
load_dotenv()

# Get MySQL credentials from .env
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

# 1. Connect to local MySQL server
conn = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD
)
cursor = conn.cursor()

# 2. Create database (if not exists)
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE}")
cursor.execute(f"USE {MYSQL_DATABASE}")

# 3. Create table (if not exists)
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    reasons JSON NOT NULL,
    picture VARCHAR(255)
)
""")

# 4. Student class
class Student:
    def __init__(self, name, reasons, picture):
        self.name = name
        self.reasons = reasons  # List
        self.picture = picture

    def save_to_db(self):
        sql = "INSERT INTO students (name, reasons, picture) VALUES (%s, %s, %s)"
        vals = (self.name, json.dumps(self.reasons), self.picture)
        cursor.execute(sql, vals)
        conn.commit()
        print(f"Student '{self.name}' added.")

# 5. Example usage
if __name__ == "__main__":
    # Example student
    student1 = Student(
        name="Chris",
        reasons=["Improve written communication Skills", "Expand my vocabulary"],
        picture="/images/chris.jpg"
    )
    student1.save_to_db()

    # View all students
    cursor.execute("SELECT * FROM students")
    for row in cursor.fetchall():
        print(row)

# 6. Close connection
cursor.close()
conn.close()