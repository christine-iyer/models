The errors you're encountering indicate that MySQL is rejecting the connection for both the root user and the edithbird5@gmail.com user. Let's address the issues step by step:

1. Fix the root User Connection
The error for the root user suggests that the password is incorrect or not set up properly. If you don't need to use the root user in your script, you can skip this step. Otherwise:

a. Reset the root Password
Log in to MySQL as root:

```mysql -u root -p```

If you don't know the password, follow the steps to reset it:

```mysqld_safe --skip-grant-tables
mysql -u root
ALTER USER 'root'@'localhost' IDENTIFIED BY 'NewRootPassword';FLUSH PRIVILEGES;```

b. Update your script to use the correct root credentials:

```conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="NewRootPassword",
)```

2. Fix the edithbird5@gmail.com User Connection
The error for edithbird5@gmail.com suggests either:

The password is incorrect.
The user is not properly configured in MySQL.
a. Verify the User in MySQL
Log in to MySQL as root:

```mysql -u root -p```

Check the user and plugin:

```SELECT user, host, plugin FROM mysql.user WHERE user = 'edithbird5@gmail.com';```

If the plugin is caching_sha2_password, change it to mysql_native_password:

```ALTER USER 'edithbird5@gmail.com'@'localhost' IDENTIFIED WITH 'mysql_native_password' BY 'ConfidenceClub!!';
FLUSH PRIVILEGES;```

Ensure the user has the correct privileges:

```GRANT ALL PRIVILEGES ON students_db.* TO 'edithbird5@gmail.com'@'localhost';
FLUSH PRIVILEGES;
```

3. Update the Script
Ensure your script uses the correct credentials for edithbird5@gmail.com:
```conn = mysql.connector.connect(
    host="localhost",
    user="edithbird5@gmail.com",
    password="ConfidenceClub!!",
)```

4. Debugging Tips
If the issue persists:

```mysql -u 'edithbird5@gmail.com' -p```

Test the connection manually using the MySQL CLI:

Enter the password ConfidenceClub!! when prompted. If this fails, the issue is with the MySQL user configuration.

Test the connection in Python:

```import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="edithbird5@gmail.com",
        password="ConfidenceClub!!",
    )
    print("✅ Connected to MySQL!")
except mysql.connector.Error as err:
    print(f"❌ Failed to connect: {err}")```

5. Address the SQLAlchemy Warning
The warning about declarative_base() is due to a deprecation in SQLAlchemy 2.0. Update your import to:

```from sqlalchemy.orm import declarative_base
Base = declarative_base()```

6. Final Steps
Ensure the MySQL server is running:

Run the script again:
```brew services start mysql```

Let me know if you encounter further issues!