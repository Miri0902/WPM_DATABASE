# import sqlite3
# import hashlib
# from prettytable import PrettyTable
#
# class SuperAdmin:
#     def __init__(self, userID, user, role, email, username, password, db_filename):
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
#         return hashlib.sha256(str(password).encode()).hexdigest()
#
#     def register_user(self):
#         print("Enter user details:")
#         self.user = input("User: ")
#         self.role = input("Role: ")
#         self.email = input("Email: ")
#         self.username = input("Username: ")
#         self.password = input("Password: ")
#
#         hashed_password = self.hash_password(self.password)
#
#         with sqlite3.connect(self.db_filename) as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 INSERT INTO users (User, role, email, username, password)
#                 VALUES (?, ?, ?, ?, ?)
#             ''', (self.user, self.role, self.email, self.username, hashed_password))
#             conn.commit()
#             print(f"User {self.username} registered successfully!")
#
#     def login(self, enter_username, enter_password):
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
#     def add_project(self, project_name, task, task_description, user, userid, status, percentage, start_date, end_date):
#         if not project_name or not task or not task_description or not user or not userid or not status or not start_date or not end_date:
#             print("Project details cannot have None values or be empty. Please enter all details.")
#             return
#
#         with sqlite3.connect(self.db_filename) as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 INSERT INTO projects (projectName, task, taskDescription, user, userID, role, email, status, percentage, startDate, endDate)
#                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#             ''', (project_name, task, task_description, user, userid, self.role, self.email, status, percentage,
#                   start_date, end_date))
#             conn.commit()
#
#     def load_projects_from_db(self):
#         print(f"Loading projects from database: {self.db_filename}")
#         with sqlite3.connect(self.db_filename) as conn:
#             cursor = conn.cursor()
#             cursor.execute("SELECT * FROM projects")
#             self.columns = [col[0] for col in cursor.description]
#             self.projects = [{self.columns[i]: row[i] for i in range(len(self.columns))} for row in cursor.fetchall()]
#
#     def display_projects(self, project_name=None):
#         if self.authenticated:
#             print('Available Projects:')
#             if project_name:
#                 projects_to_display = [project for project in self.projects if project.get('projectName') == project_name]
#             else:
#                 projects_to_display = self.projects
#
#             # Print Database Column Names
#             print("Database Column Names:", self.columns)
#
#             table = PrettyTable(self.columns)
#             for project in projects_to_display:
#                 table.add_row([project.get(col, '') for col in self.columns])
#
#             print(table)
#         else:
#             print("Not authorized. Incorrect username or password")
#
#     def update_project(self, project_id):
#         if not self.authenticated or self.role != 'SuperAdmin':
#             print("You are not authorized to update projects.")
#             return
#
#         with sqlite3.connect(self.db_filename) as conn:
#             cursor = conn.cursor()
#             cursor.execute("SELECT * FROM projects WHERE projectID = ?", (project_id,))
#             project_data = cursor.fetchone()
#
#             if project_data:
#                 project = dict(zip(self.columns, project_data))
#
#                 print(f"Updating ProjectID {project_id}:")
#
#                 # Display project details
#                 self.display_projects()
#
#                 update_percentage = input(
#                     f"Do you want to update the percentage for ProjectID {project_id}? (yes/no): ").lower()
#                 if update_percentage == 'yes':
#                     new_percentage = int(input(f"Enter new percentage status for ProjectID {project_id} (0-100%): "))
#                     if 0 <= new_percentage <= 100:
#                         project['percentage'] = new_percentage
#                         cursor.execute(f"UPDATE projects SET percentage = ? WHERE projectID = ?",
#                                        (new_percentage, project_id))
#                         conn.commit()
#
#                         # Update status based on percentage
#                         new_status = "Not Started"
#                         if new_percentage > 0:
#                             new_status = "In Progress"
#                         if new_percentage == 100:
#                             new_status = "Complete"
#
#                         cursor.execute(f"UPDATE projects SET status = ? WHERE projectID = ?", (new_status, project_id))
#                         conn.commit()
#
#                         if new_percentage == 100:
#                             # Send email notification
#                             subject = f"Project {project_id} Completed"
#                             body = f"Congratulations! The project {project_id} has been completed."
#
#                             self.send_and_display_notification(project_id, subject, body)
#
#                             print(f"Project Percentage for ProjectID {project_id} updated to {new_percentage}%.")
#                             print(f"Project Status for ProjectID {project_id} updated to {new_status}.")
#                             print(f"Email notification sent to the user.")
#                         else:
#                             print(f"Project Percentage for ProjectID {project_id} updated to {new_percentage}%.")
#                             print(f"Project Status for ProjectID {project_id} updated to {new_status}.")
#                     else:
#                         print("Invalid input. Percentage progress must be between 0 and 100.")
#
#                 update_description = input(
#                     f"Do you want to add or update the task description for ProjectID {project_id}? (yes/no): ").lower()
#                 if update_description == 'yes':
#                     new_description = input(f"Enter new task description for ProjectID {project_id}: ")
#                     project['taskDescription'] = new_description
#                     cursor.execute(f"UPDATE projects SET taskDescription = ? WHERE projectID = ?",
#                                    (new_description, project_id))
#                     conn.commit()
#                     print(f"Task description for ProjectID {project_id} updated.")
#
#             else:
#                 print(f"Project with ProjectID {project_id} not found.")
#
#     def send_email(self, to_email, subject, body):
#         print(f"Simulating email notification to: {to_email}")
#         print(f"Subject: {subject}")
#         print(f"Body: {body}")
#
#     def send_and_display_notification(self, project_id, subject, body):
#         user_email = self.get_user_email(project_id)
#
#         if user_email:
#             self.send_email(user_email, subject, body)
#             print(f"Email notification sent to {user_email}.")
#             print(f"Email notification sent to SuperAdmin.")
#         else:
#             print("User email not found. Email notification not sent.")
#
#     def get_user_email(self, project_id):
#         with sqlite3.connect(self.db_filename) as conn:
#             cursor = conn.cursor()
#             user_email = cursor.execute("SELECT email FROM projects WHERE projectID = ?", (project_id,)).fetchone()
#
#         return user_email[0] if user_email else None
#
#
# # Example usage
# if __name__ == "__main__":
#     db_filename = "wpm_database.db"
#
#     user1 = SuperAdmin(
#         userID=1240,
#         user='Tom Becker',
#         role='SuperAdmin',
#         email='tom.becker@ntu.ac.uk',
#         username='tomb',
#         password=123,  # Replace with your actual password
#         db_filename=db_filename
#     )
#
#     user1.create_tables()
#
#     register_new_user = input("Do you want to register a new user? (yes/no): ").lower()
#     if register_new_user == 'yes':
#         user1.register_user()
#
#     login_success = False
#
#     while not login_success:
#         # Login Simulation
#         username_input = input('Enter your username: ')
#         password_input = input('Enter your password: ')
#
#         if user1.login(username_input, password_input):
#             print("Login successful.")
#
#             # Adding or Updating a project
#             add_new_project = input("Do you want to add a new project? (yes/no): ").lower()
#             if add_new_project == 'yes':
#                 project_name = input("Enter project name: ")
#                 task = input("Enter task: ")
#                 task_description = input("Enter task description: ")
#                 user = input("Enter user: ")
#                 userid = input("Enter UserID: ")
#
#                 status = input("Enter status: ")
#                 percentage = int(input("Enter percentage: "))
#                 start_date = input("Enter start date: ")
#                 end_date = input("Enter end date: ")
#
#                 user1.add_project(project_name, task, task_description, user, userid, status, percentage, start_date, end_date)
#
#             update_existing_project = input("Do you want to update an existing project? (yes/no): ").lower()
#             if update_existing_project == 'yes':
#                 # Display available projects
#                 user1.load_projects_from_db()
#                 user1.display_projects()
#
#                 project_id_to_update = input("Enter the ProjectID you want to update: ")
#                 user1.update_project(project_id_to_update)
#
#             user1.load_projects_from_db()
#             user1.display_projects()
#             login_success = True
#         else:
#             print("Login failed. Please check your username and password.")

####################            displays the users, and projects  - however, allos empty cells  #############################

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

    def register_user(self):
        print("Enter user details:")
        self.user = input("User: ")
        self.role = input("Role: ")
        self.email = input("Email: ")
        self.username = input("Username: ")
        self.password = input("Password: ")

        hashed_password = self.hash_password(self.password)

        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (User, role, email, username, password)
                VALUES (?, ?, ?, ?, ?)
            ''', (self.user, self.role, self.email, self.username, hashed_password))
            conn.commit()
            print(f"User {self.username} registered successfully!")

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

    def add_project(self, project_name, task, task_description, user, userid, status, percentage, start_date, end_date):
        if not project_name or not task or not task_description or not user or not userid or not status or not start_date or not end_date:
            print("Project details cannot have None values or be empty. Please enter all details.")
            return

        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO projects (projectName, task, taskDescription, user, userID, role, email, status, percentage, startDate, endDate)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (project_name, task, task_description, user, userid, self.role, self.email, status, percentage,
                  start_date, end_date))
            conn.commit()

    def load_projects_from_db(self):
        print(f"Loading projects from database: {self.db_filename}")
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM projects")
            self.columns = [col[0] for col in cursor.description]
            self.projects = [{self.columns[i]: row[i] for i in range(len(self.columns))} for row in cursor.fetchall()]

    def display_projects(self, project_name=None):
        if self.authenticated:
            print('Available Projects:')
            if project_name:
                projects_to_display = [project for project in self.projects if project.get('projectName') == project_name]
            else:
                projects_to_display = self.projects

            # Print Database Column Names
            print("Database Column Names:", self.columns)

            table = PrettyTable(self.columns)
            for project in projects_to_display:
                table.add_row([project.get(col, '') for col in self.columns])

            print(table)
        else:
            print("Not authorized. Incorrect username or password")

    def update_project(self, project_id):
        if not self.authenticated or self.role != 'SuperAdmin':
            print("You are not authorized to update projects.")
            return

        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM projects WHERE projectID = ?", (project_id,))
            project_data = cursor.fetchone()

            if project_data:
                project = dict(zip(self.columns, project_data))

                print(f"Updating ProjectID {project_id}:")

                # Display project details
                self.display_projects()

                update_percentage = input(
                    f"Do you want to update the percentage for ProjectID {project_id}? (yes/no): ").lower()
                if update_percentage == 'yes':
                    new_percentage = int(input(f"Enter new percentage status for ProjectID {project_id} (0-100%): "))
                    if 0 <= new_percentage <= 100:
                        project['percentage'] = new_percentage
                        cursor.execute(f"UPDATE projects SET percentage = ? WHERE projectID = ?",
                                       (new_percentage, project_id))
                        conn.commit()

                        # Update status based on percentage
                        new_status = "Not Started"
                        if new_percentage > 0:
                            new_status = "In Progress"
                        if new_percentage == 100:
                            new_status = "Complete"

                        cursor.execute(f"UPDATE projects SET status = ? WHERE projectID = ?", (new_status, project_id))
                        conn.commit()

                        print(f"Project Percentage for ProjectID {project_id} updated to {new_percentage}%.")
                        print(f"Project Status for ProjectID {project_id} updated to {new_status}.")
                    else:
                        print("Invalid input. Percentage progress must be between 0 and 100.")

                update_description = input(
                    f"Do you want to add or update the task description for ProjectID {project_id}? (yes/no): ").lower()
                if update_description == 'yes':
                    new_description = input(f"Enter new task description for ProjectID {project_id}: ")
                    project['taskDescription'] = new_description
                    cursor.execute(f"UPDATE projects SET taskDescription = ? WHERE projectID = ?",
                                   (new_description, project_id))
                    conn.commit()
                    print(f"Task description for ProjectID {project_id} updated.")

                # Update status and send email notification if percentage is 100
                if project['percentage'] == 100 and project['status'] != 'Complete':
                    self.send_email_notification(project['email'], project['projectName'])

            else:
                print(f"Project with ProjectID {project_id} not found.")

    def view_users(self):
        if not self.authenticated or self.role != 'SuperAdmin':
            print("You are not authorized to view users.")
            return

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

    def send_email_notification(self, to_email, project_name):
        print(f"Simulating email notification to: {to_email}")
        print(f"Subject: Project {project_name} Completed")
        print(f"Body: Your project {project_name} has been completed. Congratulations!")

    def send_and_display_notification(self, to_email, project_name):
        self.send_email_notification(to_email, project_name)
        print(f"Email notification sent to {to_email}.")

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

    user1.create_tables()

    register_new_user = input("Do you want to register a new user? (yes/no): ").lower()
    if register_new_user == 'yes':
        user1.register_user()

    login_success = False

    while not login_success:
        # Login Simulation
        username_input = input('Enter your username: ')
        password_input = input('Enter your password: ')

        if user1.login(username_input, password_input):
            print("Login successful.")

            # Adding or Updating a project
            add_new_project = input("Do you want to add a new project? (yes/no): ").lower()
            if add_new_project == 'yes':
                project_name = input("Enter project name: ")
                task = input("Enter task: ")
                task_description = input("Enter task description: ")
                user = input("Enter user: ")
                userid = input("Enter UserID: ")

                status = input("Enter status: ")
                percentage = int(input("Enter percentage: "))
                start_date = input("Enter start date: ")
                end_date = input("Enter end date: ")

                user1.add_project(project_name, task, task_description, user, userid, status, percentage, start_date, end_date)

            update_existing_project = input("Do you want to update an existing project? (yes/no): ").lower()
            if update_existing_project == 'yes':
                # Display available projects
                user1.load_projects_from_db()
                user1.display_projects()

                project_id_to_update = input("Enter the ProjectID you want to update: ")
                user1.update_project(project_id_to_update)

            # View registered users
            view_users_option = input("Do you want to view all registered users? (yes/no): ").lower()
            if view_users_option == 'yes':
                user1.view_users()

            user1.load_projects_from_db()
            user1.display_projects()
            login_success = True
        else:
            print("Login failed. Please check your username and password.")

