import sqlite3
import hashlib
from PyQt6.QtWidgets import QMainWindow, QApplication
import sys
from TTCLoginpage import Ui_MainWindow

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

class SuperAdmin(TeamMembers):
    def __init__(self, userID, user, role, email, username, password, db_filename):
        super().__init__(userID, user, role, email, username, password, db_filename)

if __name__ == "__main__":
    db_filename = "wpm_database.db"

    user1 = SuperAdmin(
        userID=1240,
        user='Miroslava Ezel',
        role='SuperAdmin',
        email='n1161732@my.ntu.ac.uk',
        username='mirkae',
        password=2309,  # Replace with your actual password
        db_filename=db_filename
    )

    user1.create_tables()

    class Login(QMainWindow, Ui_MainWindow):
        def __init__(self, team_member_instance):
            super(Login, self).__init__()
            self.setupUi(self)  # This initializes the UI from TTCLoginpage.py
            self.team_member_instance = team_member_instance

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

                # Close the login page when login is successful
                self.close()
            else:
                print("Login failed. Please check your username and password.")


    app = QApplication(sys.argv)

    # Show the login page
    login_page = Login(team_member_instance=user1)
    login_page.show()

    sys.exit(app.exec())


# class Login():
#     def __init__(self):
#         super(LOgin, self).__init__()
#         loadUi("Python_WPM_draftfiles/TTCLoginpage.ui",self)
#         widget.setFixedWidth(400)
#         widget.setFixedHeight(300)
#         self.loginPushbutton.clicked.connet(self.loginfunction)
