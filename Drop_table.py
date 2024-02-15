import sqlite3
import hashlib
from prettytable import PrettyTable

class TeamMembers:
    def __init__(self, userID, user, role, email, username, password, db_filename):
        self.userID = userID
        self.user = user
        self.role = role
        self.email = email
        self.username = username
        self.password = password
        self.authenticated = False
        self.db_filename = db_filename
        self.columns = []  # To store column names
        self.projects = []

    def create_tables(self):
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()

            # Modify the CREATE TABLE statement to use "user" instead of "Name"
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    userID INTEGER PRIMARY KEY,
                    user TEXT,  -- Change from "Name" to "user"
                    role TEXT,
                    email TEXT,
                    username TEXT,
                    password TEXT
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS projects (
                    projectID INTEGER PRIMARY KEY,
                    projectName TEXT,
                    task TEXT,
                    taskDescription TEXT,
                    user TEXT,
                    userID INTEGER,
                    username TEXT,
                    role TEXT,
                    email TEXT,
                    status TEXT,
                    percentage INTEGER,
                    startDate TEXT,
                    endDate TEXT,
                    FOREIGN KEY(userID) REFERENCES users(userID)
                )
            ''')

            conn.commit()

    def hash_password(self, password):
        return hashlib.sha256(str(password).encode()).hexdigest()

    def rename_column(self):
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()

            # Create a temporary table with the new column name
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS temp_users (
                    userID INTEGER PRIMARY KEY,
                    user TEXT,
                    role TEXT,
                    email TEXT,
                    username TEXT,
                    password TEXT
                )
            ''')

            # Copy data from the old table to the temporary table
            cursor.execute('''
                INSERT INTO temp_users SELECT * FROM users
            ''')

            # Drop the old table
            cursor.execute('''
                DROP TABLE IF EXISTS users
            ''')

            # Rename the temporary table to the original table name
            cursor.execute('''
                ALTER TABLE temp_users RENAME TO users
            ''')

            # Commit the changes
            conn.commit()

# Example usage
if __name__ == "__main__":
    db_filename = "wpm_database.db"

    user1 = TeamMembers(
        userID=1240,
        user='Miroslava Ezel',
        role='SuperAdmin',
        email='n1161732@my.ntu.ac.uk',
        username='mirkae',
        password=2309,  # Replace with your actual password
        db_filename=db_filename
    )

    user1.rename_column()  # Call this method to rename the existing schema

    user1.create_tables()  # Call this method to create tables with the updated schema

    # Rest of your script remains unchanged...
