# import sqlite3
# import hashlib
# from prettytable import PrettyTable
# from PyQt6 import QtWidgets
# from PyQt6.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox
# from TTCLoginpage import Ui_MainWindow as UiLogin
# from RegisteredUsers import Ui_MainWindow as UiRegistered
# import sys
#
#
# class TeamMembers:
#     """
#     Clsss representing team members.
#     """
#     def __init__(self, userID, user, role, email, username, password, db_filename):
#         """
#         Initialise a TeamMembers instance.
#
#         :param userID: UserID
#         :param user: User's name
#         :param role: User's role
#         :param email: User's email
#         :param username: User's username
#         :param password: User's password
#         :param db_filename: Database filename
#         """
#         self.userID = userID
#         self.user = user
#         self.role = role
#         self.email = email
#         self.username = username
#         self.password = password
#         self.authenticated = False
#         self.db_filename = db_filename
#         self.columns = []  # To store column names
#         self.projects = []
#
#     def create_tables(self):
#         """
#         Create tables 'users' and 'projoects' in the database.
#         """
#         with sqlite3.connect(self.db_filename) as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 CREATE TABLE IF NOT EXISTS users (
#                     userID INTEGER PRIMARY KEY,
#                     user TEXT,
#                     role TEXT,
#                     email TEXT,
#                     username TEXT,
#                     password TEXT
#                 )
#             ''')
#
#             cursor.execute('''
#                 CREATE TABLE IF NOT EXISTS projects (
#                     projectID INTEGER PRIMARY KEY,
#                     projectName TEXT,
#                     task TEXT,
#                     taskDescription TEXT,
#                     user TEXT,
#                     userID INTEGER,
#                     username TEXT,
#                     role TEXT,
#                     email TEXT,
#                     status TEXT,
#                     percentage INTEGER,
#                     startDate TEXT,
#                     endDate TEXT,
#                     FOREIGN KEY(userID) REFERENCES users(userID)
#                 )
#             ''')
#
#             conn.commit()
#
#     def hash_password(self, password):
#         """
#         Hash the provided password.
#
#         :param password: Password to has
#         :return: Hashed password
#         """
#         return hashlib.sha256(str(password).encode()).hexdigest()
#
#     def validate_input(self, prompt, allow_empty=False):
#         """
#         Validate user input.
#
#         :param prompt: Prompt message
#         :param allow_empty: Whether empty input is allowed
#         :return: Validated user input
#         """
#         while True:
#             user_input = input(prompt).strip()
#             if allow_empty or user_input:
#                 return user_input
#             else:
#                 print("Input cannot be empty. Please enter a value.")
#
#     def view_existing_projects(self):
#
#         pass
#
#
# class SuperAdmin(TeamMembers):
#     """
#     Class representing a SuperAdmin, inheriting from TeamMembers.
#     """
#     def __init__(self, userID, user, role, email, username, password, db_filename):
#         """
#         Initialise a SuperAdmin instance.
#
#         :param userID: UserID
#         :param user: User's name
#         :param role: User's role
#         :param email: User's email
#         :param username: User's username
#         :param password: User's password
#         :param db_filename: Database filename
#         """
#         super().__init__(userID, user, role, email, username, password, db_filename)
#
#     def login(self, enter_username, enter_password):
#         """
#         Perform login for a SuperAdmin
#
#         :param enter_username: Entered username
#         :param enter_password: Entered password
#         :return: bool: True if login is succesful, False is not.
#         """
#
#         hashed_password = self.hash_password(enter_password)
#
#         with sqlite3.connect(self.db_filename) as conn:
#             cursor = conn.cursor()
#             cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (enter_username, hashed_password))
#
#             user_data = cursor.fetchone()
#
#         if user_data:
#             self.authenticated = True
#             self.userID = user_data[0]
#             self.user = user_data[1]
#             self.role = user_data[2]
#             self.email = user_data[3]
#             self.username = user_data[4]
#             return True
#         else:
#             return False
#
#
# class Login(QMainWindow, UiLogin):
#     """
#     Class representing the login page GUI.
#     """
#     def __init__(self, team_member_instance):
#         """
#         Initialise the Login instance
#
#         :param team_member_instance: Instance of TeamMembers
#         """
#         super(Login, self).__init__()
#         self.setupUi(self)  # This initializes the UI from TTCLoginpage.py
#         self.team_member_instance = team_member_instance
#         self.RegisteredUsersPage = None  # Create a variable to hold the RegisteredUsersPage instance
#
#         # Connect login button to the login function
#         self.LoginPushbutton.clicked.connect(self.login_function)
#
#     def login_function(self):
#         """
#         Perform login when the LoginPushbutton is clicked.
#         :return:
#         """
#         enter_username = self.lineEdit.text()
#         enter_password = self.lineEdit_2.text()
#
#         # logic using the TeamMembers instance
#         hashed_password = self.team_member_instance.hash_password(enter_password)
#
#         with sqlite3.connect(self.team_member_instance.db_filename) as conn:
#             cursor = conn.cursor()
#             cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (enter_username, hashed_password))
#
#             user_data = cursor.fetchone()
#
#         if user_data:
#             self.team_member_instance.authenticated = True
#             self.team_member_instance.userID = user_data[0]
#             self.team_member_instance.user = user_data[1]
#             self.team_member_instance.role = user_data[2]
#             self.team_member_instance.email = user_data[3]
#             self.team_member_instance.username = user_data[4]
#             print("Login successful.")
#
#             # Create and show the Registered Users page after successful login
#             if not self.RegisteredUsersPage:
#                 view_users_instance = ViewUsers(self.team_member_instance.db_filename)
#                 self.RegisteredUsersPage = RegisteredUsers(view_users_instance=view_users_instance)
#             self.RegisteredUsersPage.show()
#
#             # Close the login page when login is successful
#             self.close()
#         else:
#             print("Login failed. Please check your username and password.")
#
#
# class ViewUsers:
#     """
#     Class responsible for viewing registered users.
#     """
#     def __init__(self, db_filename):
#         """
#         Initialise the ViewUsers instance.
#         :param db_filename: Database filename
#         """
#         self.db_filename = db_filename
#
#     def view_users(self):
#         """
#         View the registered users and dispaly their information.
#         """
#         with sqlite3.connect(self.db_filename) as conn:
#             cursor = conn.cursor()
#             cursor.execute("SELECT userID, user, role, email FROM users")
#             users_data = cursor.fetchall()
#
#             if not users_data:
#                 print("No registered users found.")
#                 return
#
#             columns = ["UserID", "User", "Role", "Email"]
#             table = PrettyTable(columns)
#             for user_data in users_data:
#                 table.add_row(user_data)
#
#             print("Registered Users:")
#             print(table)
#
#
# class RegisteredUsers(QMainWindow, UiRegistered):
#     """
#     Class representing the Registered Users page GUI.
#     """
#     def __init__(self, view_users_instance):
#         """
#         Initialise the RegisteredUsers instance.
#
#         :param view_users_instance: Instance of ViewUsers
#         """
#         super(RegisteredUsers, self).__init__()
#         self.setupUi(self)  # This initializes the UI from RegisteredUsers.py
#         self.view_users_instance = view_users_instance
#
#
#
#         # Connect the view users button to the view_users_function
#         self.viewUsersButton.clicked.connect(self.view_users_function)
#
#     def view_users_function(self):
#         """
#         Call the view_users method to from the ViewUsers instance.
#
#         """
#         # Call the view_users method from the ViewUsers instance
#         self.view_users_instance.view_users()
#
#
# if __name__ == "__main__":
#     db_filename = "wpm_database.db"
#
#     user1 = SuperAdmin(
#         userID=1240,
#         user='Miroslava Ezel',
#         role='SuperAdmin',
#         email='n1161732@my.ntu.ac.uk',
#         username='mirkae',
#         password=2309,
#         db_filename=db_filename
#     )
#
#     user1.create_tables()
#
#     app = QApplication([])
#
#     # Show the login page
#     login_page = Login(team_member_instance=user1)
#     login_page.show()
#
#
#     sys.exit(app.exec())
#



###################################################   login works, also brings the registeredUsers gui, however, does not asks for users inputs and the table ##################################


# import sqlite3
# import hashlib
# from prettytable import PrettyTable
# from PyQt6 import QtWidgets, QtGui, QtCore
# from PyQt6.QtWidgets import QMainWindow, QApplication
# from TTCLoginpage import Ui_MainWindow as UiLogin
# from RegisteredUsers import Ui_MainWindow as UiRegistered
# import sys
#
#
# class TeamMembers:
#     """
#     Class representing team members.
#     """
#     def __init__(self, userID, user, role, email, username, password, db_filename):
#         """
#         Initialise a TeamMembers instance.
#
#         :param userID: UserID
#         :param user: User's name
#         :param role: User's role
#         :param email: User's email
#         :param username: User's username
#         :param password: User's password
#         :param db_filename: Database filename
#         """
#         self.userID = userID
#         self.user = user
#         self.role = role
#         self.email = email
#         self.username = username
#         self.password = password
#         self.authenticated = False
#         self.db_filename = db_filename
#         self.columns = []  # To store column names
#         self.projects = []
#
#     def create_tables(self):
#         """
#         Create tables 'users' and 'projects' in the database.
#         """
#         with sqlite3.connect(self.db_filename) as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 CREATE TABLE IF NOT EXISTS users (
#                     userID INTEGER PRIMARY KEY,
#                     user TEXT,
#                     role TEXT,
#                     email TEXT,
#                     username TEXT,
#                     password TEXT
#                 )
#             ''')
#
#             cursor.execute('''
#                 CREATE TABLE IF NOT EXISTS projects (
#                     projectID INTEGER PRIMARY KEY,
#                     projectName TEXT,
#                     task TEXT,
#                     taskDescription TEXT,
#                     user TEXT,
#                     userID INTEGER,
#                     username TEXT,
#                     role TEXT,
#                     email TEXT,
#                     status TEXT,
#                     percentage INTEGER,
#                     startDate TEXT,
#                     endDate TEXT,
#                     FOREIGN KEY(userID) REFERENCES users(userID)
#                 )
#             ''')
#
#             conn.commit()
#
#     def hash_password(self, password):
#         """
#         Hash the provided password.
#
#         :param password: Password to hash
#         :return: Hashed password
#         """
#         return hashlib.sha256(str(password).encode()).hexdigest()
#
#     def validate_input(self, prompt, allow_empty=False):
#         """
#         Validate user input.
#
#         :param prompt: Prompt message
#         :param allow_empty: Whether empty input is allowed
#         :return: Validated user input
#         """
#         while True:
#             user_input = input(prompt).strip()
#             if allow_empty or user_input:
#                 return user_input
#             else:
#                 print("Input cannot be empty. Please enter a value.")
#
#     def view_existing_projects(self):
#         pass
#
#
# class SuperAdmin(TeamMembers):
#     """
#     Class representing a SuperAdmin, inheriting from TeamMembers.
#     """
#     def __init__(self, userID, user, role, email, username, password, db_filename):
#         """
#         Initialise a SuperAdmin instance.
#
#         :param userID: UserID
#         :param user: User's name
#         :param role: User's role
#         :param email: User's email
#         :param username: User's username
#         :param password: User's password
#         :param db_filename: Database filename
#         """
#         super().__init__(userID, user, role, email, username, password, db_filename)
#
#     def login(self, enter_username, enter_password):
#         """
#         Perform login for a SuperAdmin
#
#         :param enter_username: Entered username
#         :param enter_password: Entered password
#         :return: bool: True if login is successful, False if not.
#         """
#
#         hashed_password = self.hash_password(enter_password)
#
#         with sqlite3.connect(self.db_filename) as conn:
#             cursor = conn.cursor()
#             cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (enter_username, hashed_password))
#
#             user_data = cursor.fetchone()
#
#         if user_data:
#             self.authenticated = True
#             self.userID = user_data[0]
#             self.user = user_data[1]
#             self.role = user_data[2]
#             self.email = user_data[3]
#             self.username = user_data[4]
#             return True
#         else:
#             return False
#
#
# class Login(QMainWindow, UiLogin):
#     """
#     Class representing the login page GUI.
#     """
#     def __init__(self, team_member_instance, registered_users_page):
#         """
#         Initialise the Login instance
#
#         :param team_member_instance: Instance of TeamMembers
#         :param registered_users_page: Instance of RegisteredUsers
#         """
#         super(Login, self).__init__()
#         self.setupUi(self)  # This initializes the UI from TTCLoginpage.py
#         self.team_member_instance = team_member_instance
#         self.registered_users_page = registered_users_page
#
#         # Connect login button to the login function
#         self.LoginPushbutton.clicked.connect(self.login_function)
#
#     def login_function(self):
#         """
#         Perform login when the LoginPushbutton is clicked.
#         :return:
#         """
#         enter_username = self.lineEdit.text()
#         enter_password = self.lineEdit_2.text()
#
#         # logic using the TeamMembers instance
#         hashed_password = self.team_member_instance.hash_password(enter_password)
#
#         with sqlite3.connect(self.team_member_instance.db_filename) as conn:
#             cursor = conn.cursor()
#             cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (enter_username, hashed_password))
#
#             user_data = cursor.fetchone()
#
#         if user_data:
#             self.team_member_instance.authenticated = True
#             self.team_member_instance.userID = user_data[0]
#             self.team_member_instance.user = user_data[1]
#             self.team_member_instance.role = user_data[2]
#             self.team_member_instance.email = user_data[3]
#             self.team_member_instance.username = user_data[4]
#             print("Login successful.")
#
#             # Show the Registered Users page after a successful login
#             self.registered_users_page.show()
#
#             # Close the login page when login is successful
#             self.close()
#         else:
#             print("Login failed. Please check your username and password.")
#
#
# class ViewUsers:
#     """
#     Class responsible for viewing registered users.
#     """
#     def __init__(self, db_filename):
#         """
#         Initialise the ViewUsers instance.
#         :param db_filename: Database filename
#         """
#         self.db_filename = db_filename
#
#     def view_users(self):
#         """
#         View the registered users and display their information.
#         """
#         with sqlite3.connect(self.db_filename) as conn:
#             cursor = conn.cursor()
#             cursor.execute("SELECT userID, user, role, email FROM users")
#             users_data = cursor.fetchall()
#
#             if not users_data:
#                 print("No registered users found.")
#                 return
#
#             columns = ["UserID", "User", "Role", "Email"]
#             table = PrettyTable(columns)
#             for user_data in users_data:
#                 table.add_row(user_data)
#
#             print("Registered Users:")
#             print(table)
#
#
# class RegisteredUsers(QMainWindow, UiRegistered):
#     """
#     Class representing the Registered Users page GUI.
#     """
#     def __init__(self, view_users_instance, update_users_instance, add_users_instance):
#         """
#         Initialise the RegisteredUsers instance.
#
#         :param view_users_instance: Instance of ViewUsers
#         :param update_users_instance: Instance of UpdateExistingUsers
#         :param add_users_instance: Instance of RegisterUser
#         """
#         super(RegisteredUsers, self).__init__()
#         self.setupUi(self)  # This initializes the UI from RegisteredUsers.py
#         self.view_users_instance = view_users_instance
#         self.update_users_instance = update_users_instance
#         self.add_users_instance = add_users_instance
#
#         # Connect the view users button to the view_users_function
#         self.viewUserButton.clicked.connect(self.view_users_function)
#         self.updateUserButton.clicked.connect(self.update_users_function)
#         self.addUserButton.clicked.connect(self.add_users_function)
#
#     def view_users_function(self):
#         """
#         Call the view_users method from the ViewUsers instance.
#         """
#         # Call the view_users method from the ViewUsers instance
#         self.view_users_instance.view_users()
#
#     def update_users_function(self):
#         """
#         Call the update_existing_user method from the UpdateExistingUsers instance.
#         """
#         # Call the update_existing_user method from the UpdateExistingUsers instance
#         self.update_users_instance.update_existing_user()
#
#     def add_users_function(self):
#         """
#         Call the execute method from the RegisterUser instance.
#         """
#         # Call the execute method from the RegisterUser instance
#         self.add_users_instance.execute()
#
#
# class UpdateExistingUsers:
#     def __init__(self, db_filename):
#         self.db_filename = db_filename
#
#     def update_existing_user(self):
#         while True:
#             user_id_to_update = input("Enter the UserID of the user you want to update: ")
#             user_to_update = input("Enter the username of the user you want to update:")
#
#             with sqlite3.connect(self.db_filename) as conn:
#                 cursor = conn.cursor()
#                 cursor.execute("SELECT * FROM users WHERE userID = ? AND username = ?", (user_id_to_update, user_to_update))
#                 user_data = cursor.fetchone()
#
#                 if not user_data:
#                     print(f"User with UserID {user_id_to_update} and username {user_to_update} not found.")
#                     break
#
#                 user_columns = [col[0] for col in cursor.description]
#                 user = dict(zip(user_columns, user_data))
#
#                 print(f"Updating UserID {user_id_to_update} and username {user_to_update}:")
#
#                 # Display user details
#                 columns_to_display = ["UserID", "User", "Role", "Email"]
#                 table_to_display = PrettyTable(columns_to_display)
#                 table_to_display.add_row([user.get(col, '') for col in columns_to_display])
#                 print(table_to_display)
#
#                 columns_to_update = input("Enter the columns you want to update (comma-separated): ").split(',')
#                 columns_to_update = [col.strip() for col in columns_to_update]
#
#                 for col in columns_to_update:
#                     if col not in user_columns:
#                         print(f"Invalid column '{col}'. Please choose from {', '.join(user_columns)}")
#                         break
#
#                 for col in columns_to_update:
#                     new_value = input(f"Enter new value for {col}: ").strip()
#                     cursor.execute(f"UPDATE users SET {col} = ? WHERE userID = ? AND username = ?",
#                                    (new_value, user_id_to_update, user_to_update))
#                     conn.commit()
#
#                 print(f"User details for UserID {user_id_to_update}, username {user_to_update} updated successfully.")
#
#             update_more_users = input("Do you want to update more users? (yes/no): ").lower()
#             if update_more_users != 'yes':
#                 break
#
#
# class RegisterUser:
#     def __init__(self, db_filename):
#         self.db_filename = db_filename
#
#     def validate_input(self, prompt, allow_empty=False):
#         while True:
#             user_input = input(prompt).strip()
#             if allow_empty or user_input:
#                 return user_input
#             else:
#                 print("Input cannot be empty. Please enter a value.")
#
#     def execute(self):
#         while True:
#             print("Enter user details:")
#             user = self.validate_input("User: ")
#             role = self.validate_input("Role: ")
#             email = self.validate_input("Email: ")
#             username = self.validate_input("Username: ")
#             password = self.validate_input("Password: ")
#
#             hashed_password = hashlib.sha256(str(password).encode()).hexdigest()
#
#             with sqlite3.connect(self.db_filename) as conn:
#                 cursor = conn.cursor()
#                 cursor.execute('''
#                     INSERT INTO users (user, role, email, username, password)
#                     VALUES (?, ?, ?, ?, ?)
#                 ''', (user, role, email, username, hashed_password))
#                 conn.commit()
#
#             print(f"User {user} registered successfully!")
#
#             # Ask if the user wants to add more users after completing other operations
#             add_more_users = input("Do you want to add more users? (Y/N): ").lower()
#             if add_more_users != 'y':
#                 break
#
#
# if __name__ == "__main__":
#     db_filename = "wpm_database.db"
#
#     user1 = SuperAdmin(
#         userID=1240,
#         user='Miroslava Ezel',
#         role='SuperAdmin',
#         email='n1161732@my.ntu.ac.uk',
#         username='mirkae',
#         password=2309,
#         db_filename=db_filename
#     )
#
#     user1.create_tables()
#
#     app = QApplication([])
#
#     # Create an instance of ViewUsers
#     view_users_instance = ViewUsers(db_filename)
#
#     # Create an instance of UpdateExistingUsers
#     update_users_instance = UpdateExistingUsers(db_filename)
#
#     # Create an instance of RegisterUser
#     register_user_instance = RegisterUser(db_filename)
#
#     # Show the login page
#     login_page = Login(team_member_instance=user1, registered_users_page=RegisteredUsers(view_users_instance, update_users_instance, register_user_instance))
#     login_page.show()
#
#     sys.exit(app.exec())
#
#
#

import sqlite3
import hashlib
from prettytable import PrettyTable
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QMainWindow, QApplication
from TTCLoginpage import Ui_MainWindow as UiLogin
from RegisteredUsers import Ui_MainWindow as UiRegistered
import sys

class TeamMembers:
    """
    Class representing team members.
    """
    def __init__(self, userID, user, role, email, username, password, db_filename):
        """
        Initialise a TeamMembers instance.

        :param userID: UserID
        :param user: User's name
        :param role: User's role
        :param email: User's email
        :param username: User's username
        :param password: User's password
        :param db_filename: Database filename
        """
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
        """
        Create tables 'users' and 'projects' in the database.
        """
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
        """
        Hash the provided password.

        :param password: Password to hash
        :return: Hashed password
        """
        return hashlib.sha256(str(password).encode()).hexdigest()

    def validate_input(self, prompt, allow_empty=False):
        """
        Validate user input.

        :param prompt: Prompt message
        :param allow_empty: Whether empty input is allowed
        :return: Validated user input
        """
        while True:
            user_input = input(prompt).strip()
            if allow_empty or user_input:
                return user_input
            else:
                print("Input cannot be empty. Please enter a value.")

    def view_existing_projects(self):
        pass


class SuperAdmin(TeamMembers):
    """
    Class representing a SuperAdmin, inheriting from TeamMembers.
    """
    def __init__(self, userID, user, role, email, username, password, db_filename):
        """
        Initialise a SuperAdmin instance.

        :param userID: UserID
        :param user: User's name
        :param role: User's role
        :param email: User's email
        :param username: User's username
        :param password: User's password
        :param db_filename: Database filename
        """
        super().__init__(userID, user, role, email, username, password, db_filename)

    def login(self, enter_username, enter_password):
        """
        Perform login for a SuperAdmin

        :param enter_username: Entered username
        :param enter_password: Entered password
        :return: bool: True if login is successful, False if not.
        """

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
    """
    Class representing the login page GUI.
    """
    def __init__(self, team_member_instance, registered_users_page):
        """
        Initialise the Login instance

        :param team_member_instance: Instance of TeamMembers
        :param registered_users_page: Instance of RegisteredUsers
        """
        super(Login, self).__init__()
        self.setupUi(self)  # This initializes the UI from TTCLoginpage.py
        self.team_member_instance = team_member_instance
        self.registered_users_page = registered_users_page

        # Connect login button to the login function
        self.LoginPushbutton.clicked.connect(self.login_function)

    def login_function(self):
        """
        Perform login when the LoginPushbutton is clicked.
        :return:
        """
        enter_username = self.lineEdit.text()
        enter_password = self.lineEdit_2.text()

        # logic using the TeamMembers instance
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

            # Show the Registered Users page after a successful login
            self.registered_users_page.show()

            # Close the login page when login is successful
            self.close()
        else:
            print("Login failed. Please check your username and password.")


class ViewUsers:
    """
    Class responsible for viewing registered users.
    """
    def __init__(self, db_filename):
        """
        Initialise the ViewUsers instance.
        :param db_filename: Database filename
        """
        self.db_filename = db_filename

    def view_users(self):
        """
        View the registered users and display their information.
        """
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
    """
    Class representing the Registered Users page GUI.
    """
    def __init__(self, view_users_instance, update_users_instance, add_users_instance):
        """
        Initialise the RegisteredUsers instance.

        :param view_users_instance: Instance of ViewUsers
        :param update_users_instance: Instance of UpdateExistingUsers
        :param add_users_instance: Instance of RegisterUser
        """
        super(RegisteredUsers, self).__init__()
        self.setupUi(self)  # This initializes the UI from RegisteredUsers.py
        self.view_users_instance = view_users_instance
        self.update_users_instance = update_users_instance
        self.add_users_instance = add_users_instance

        # Connect the view users button to the view_users_function
        self.viewUserButton.clicked.connect(self.view_users_function)
        self.updateUserButton.clicked.connect(self.update_users_function)
        self.addUserButton.clicked.connect(self.add_users_function)

    def view_users_function(self):
        """
        Call the view_users method from the ViewUsers instance.
        """
        # Call the view_users method from the ViewUsers instance
        self.view_users_instance.view_users()

    def update_users_function(self):
        # Get user input for UserID and username
        user_id_to_update = input("Enter the UserID of the user you want to update: ")
        user_to_update = input("Enter the username of the user you want to update: ")
        #
        # # Call the update_existing_user method from the UpdateExistingUsers instance
        # success, message = self.update_users_instance.update_existing_user(user_id_to_update, user_to_update)
        #
        # # Display the result message
        # if success:
        #     print(message)
        # else:
        #     print(message)

    # def update_users_function(self):
    #     """
    #     Call the update_existing_user method from the UpdateExistingUsers instance.
    #     """
    #     # Call the update_existing_user method from the UpdateExistingUsers instance
    #     self.update_users_instance.update_existing_user()

    def add_users_function(self):
        """
        Call the execute method from the RegisterUser instance.
        """
        # Call the execute method from the RegisterUser instance
        self.add_users_instance.execute()


class UpdateExistingUsers:
    def __init__(self, db_filename):
        self.db_filename = db_filename

    def update_existing_user(self):
        try:
            while True:
                user_id_to_update = input("Enter the UserID of the user you want to update: ")
                user_to_update = input("Enter the username of the user you want to update:")

                print(f"Attempting to update user with UserID {user_id_to_update} and username {user_to_update}...")

                with sqlite3.connect(self.db_filename) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM users WHERE userID = ? AND username = ?", (user_id_to_update, user_to_update))
                    user_data = cursor.fetchone()

                    if not user_data:
                        print(f"User with UserID {user_id_to_update}, username {user_to_update} not found.")
                        continue  # Go back to the beginning of the loop

                    user_columns = [col[0] for col in cursor.description]
                    user = dict(zip(user_columns, user_data))

                    print(f"Updating UserID {user_id_to_update} and username {user_to_update}:")

                    # Display user details
                    columns_to_display = ["UserID", "User", "Role", "Email"]
                    table_to_display = PrettyTable(columns_to_display)
                    table_to_display.add_row([user.get(col, '') for col in columns_to_display])
                    print(table_to_display)

                    columns_to_update = input("Enter the columns you want to update (comma-separated): ").split(',')
                    columns_to_update = [col.strip() for col in columns_to_update]

                    for col in columns_to_update:
                        if col not in user_columns:
                            print(f"Invalid column '{col}'. Please choose from {', '.join(user_columns)}")
                            break

                    for col in columns_to_update:
                        new_value = input(f"Enter new value for {col}: ").strip()
                        cursor.execute(f"UPDATE users SET {col} = ? WHERE userID = ? AND username = ?",
                                       (new_value, user_id_to_update, user_to_update))
                        conn.commit()

                    print(f"User details for UserID {user_id_to_update}, username {user_to_update} updated successfully.")

                update_more_users = input("Do you want to update more users? (yes/no): ").lower()
                if update_more_users != 'yes':
                    break

        except Exception as e:
            print(f"An error occurred: {e}")

class RegisterUser:
    def __init__(self, db_filename):
        self.db_filename = db_filename

    def validate_input(self, prompt, allow_empty=False):
        while True:
            user_input = input(prompt).strip()
            if allow_empty or user_input:
                return user_input
            else:
                print("Input cannot be empty. Please enter a value.")

    def execute(self):
        while True:
            print("Enter user details:")
            user = self.validate_input("User: ")
            role = self.validate_input("Role: ")
            email = self.validate_input("Email: ")
            username = self.validate_input("Username: ")
            password = self.validate_input("Password: ")

            hashed_password = hashlib.sha256(str(password).encode()).hexdigest()

            with sqlite3.connect(self.db_filename) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO users (user, role, email, username, password)
                    VALUES (?, ?, ?, ?, ?)
                ''', (user, role, email, username, hashed_password))
                conn.commit()

            print(f"User {user} registered successfully!")

            # Ask if the user wants to add more users after completing other operations
            add_more_users = input("Do you want to add more users? (Y/N): ").lower()
            if add_more_users != 'y':
                break


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
    login_success = False



    app = QApplication([])

    # Create an instance of ViewUsers
    view_users_instance = ViewUsers(db_filename)

    # Create an instance of UpdateExistingUsers
    update_users_instance = UpdateExistingUsers(db_filename)

    # Create an instance of RegisterUser
    register_user_instance = RegisterUser(db_filename)

    # Show the login page
    login_page = Login(team_member_instance=user1, registered_users_page=RegisteredUsers(view_users_instance, update_users_instance, register_user_instance))
    login_page.show()

    sys.exit(app.exec())






