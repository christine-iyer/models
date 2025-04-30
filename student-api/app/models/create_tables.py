from sqlalchemy import create_engine
from student import Student
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL is missing!")

# Set up SQLAlchemy engine
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Create all tables
def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")

if __name__ == "__main__":
    create_tables()

    import mysql.connector
import json

# 1. Connect to local MySQL server
conn = mysql.connector.connect(
    host="localhost",
    user="edithbird5@gmail.com",          # Replace with your MySQL username
    password="ConfidenceClub!!", # Replace with your MySQL password
)
cursor = conn.cursor()

# 2. Create database (if not exists)
cursor.execute("CREATE DATABASE IF NOT EXISTS school")
cursor.execute("USE school")

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
        name="Laura",
        reasons=["Edification", "Community"],
        picture="/images/laura.jpg"
    )
    student1.save_to_db()

    # View all students
    cursor.execute("SELECT * FROM students")
    for row in cursor.fetchall():
        print(row)

# 6. Close connection
cursor.close()
conn.close()