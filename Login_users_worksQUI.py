

import sqlite3
import hashlib
from prettytable import PrettyTable
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox
from TTCLoginpage import Ui_MainWindow as UiLogin
from RegisteredUsers import Ui_MainWindow as UiRegistered
import sys


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
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    userID INTEGER PRIMARY KEY,
                    user TEXT,
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

    def validate_input(self, prompt, allow_empty=False):
        while True:
            user_input = input(prompt).strip()
            if allow_empty or user_input:
                return user_input
            else:
                print("Input cannot be empty. Please enter a value.")

    def view_existing_projects(self):
        # ViewExistingProject is not defined in your code
        # Assuming you have this class defined elsewhere
        pass


class SuperAdmin(TeamMembers):
    def __init__(self, userID, user, role, email, username, password, db_filename):
        super().__init__(userID, user, role, email, username, password, db_filename)

    def login(self, enter_username, enter_password):
        hashed_password = self.hash_password(enter_password)

        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (enter_username, hashed_password))

            user_data = cursor.fetchone()

        if user_data:
            self.authenticated = True
            self.userID = user_data[0]
            self.user = user_data[1]
            self.role = user_data[2]
            self.email = user_data[3]
            self.username = user_data[4]
            return True
        else:
            return False


class Login(QMainWindow, UiLogin):
    def __init__(self, team_member_instance):
        super(Login, self).__init__()
        self.setupUi(self)  # This initializes the UI from TTCLoginpage.py
        self.team_member_instance = team_member_instance
        self.RegisteredUsersPage = None  # Create a variable to hold the RegisteredUsersPage instance

        # Connect login button to the login function
        self.LoginPushbutton.clicked.connect(self.login_function)

    def login_function(self):
        enter_username = self.lineEdit.text()
        enter_password = self.lineEdit_2.text()

        # Your login logic using the TeamMembers instance
        hashed_password = self.team_member_instance.hash_password(enter_password)

        with sqlite3.connect(self.team_member_instance.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (enter_username, hashed_password))

            user_data = cursor.fetchone()

        if user_data:
            self.team_member_instance.authenticated = True
            self.team_member_instance.userID = user_data[0]
            self.team_member_instance.user = user_data[1]
            self.team_member_instance.role = user_data[2]
            self.team_member_instance.email = user_data[3]
            self.team_member_instance.username = user_data[4]
            print("Login successful.")

            # Create and show the Registered Users page after successful login
            if not self.RegisteredUsersPage:
                view_users_instance = ViewUsers(self.team_member_instance.db_filename)
                self.RegisteredUsersPage = RegisteredUsers(view_users_instance=view_users_instance)
            self.RegisteredUsersPage.show()

            # Close the login page when login is successful
            self.close()
        else:
            print("Login failed. Please check your username and password.")


class ViewUsers:
    def __init__(self, db_filename):
        self.db_filename = db_filename

    def view_users(self):
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT userID, user, role, email FROM users")
            users_data = cursor.fetchall()

            if not users_data:
                print("No registered users found.")
                return

            columns = ["UserID", "User", "Role", "Email"]
            table = PrettyTable(columns)
            for user_data in users_data:
                table.add_row(user_data)

            print("Registered Users:")
            print(table)


class RegisteredUsers(QMainWindow, UiRegistered):
    def __init__(self, view_users_instance):
        super(RegisteredUsers, self).__init__()
        self.setupUi(self)  # This initializes the UI from RegisteredUsers.py
        self.view_users_instance = view_users_instance



        # Connect the view users button to the view_users_function
        self.viewUsersButton.clicked.connect(self.view_users_function)

    def view_users_function(self):
        # Call the view_users method from the ViewUsers instance
        self.view_users_instance.view_users()


if __name__ == "__main__":
    db_filename = "wpm_database.db"

    user1 = SuperAdmin(
        userID=1240,
        user='Miroslava Ezel',
        role='SuperAdmin',
        email='n1161732@my.ntu.ac.uk',
        username='mirkae',
        password=2309,
        db_filename=db_filename
    )

    user1.create_tables()

    app = QApplication([])

    # Show the login page
    login_page = Login(team_member_instance=user1)
    login_page.show()

    # # Show the registered users page
    # view_users_instance = ViewUsers(db_filename)
    # registered_users_page = RegisteredUsers(view_users_instance=view_users_instance)
    # registered_users_page.show()

    sys.exit(app.exec())

