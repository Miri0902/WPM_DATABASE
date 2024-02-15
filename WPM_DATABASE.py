# #
# import sqlite3
# import hashlib
# from prettytable import PrettyTable
#
# class TeamMembers:
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
#         with sqlite3.connect(self.db_filename) as conn:
#             cursor = conn.cursor()
#             cursor.execute("SELECT * FROM projects WHERE projectID = ?", (project_id,))
#             project_data = cursor.fetchone()
#
#             if project_data:
#                 project = dict(zip(self.columns, project_data))
#
#                 if self.role == 'SuperAdmin' or self.userID == project.get('userID'):
#                     print(f"Updating ProjectID {project_id}:")
#
#                     # Display project details
#                     self.display_projects()
#
#                     update_percentage = input(f"Do you want to update the percentage for ProjectID {project_id}? (yes/no): ").lower()
#                     if update_percentage == 'yes':
#                         if self.userID == project.get('userID'):
#                             new_percentage = int(input(f"Enter new percentage status for ProjectID {project_id} (0-100%): "))
#                             if 0 <= new_percentage <= 100:
#                                 project['percentage'] = new_percentage
#                                 cursor.execute(f"UPDATE projects SET percentage = ? WHERE projectID = ?", (new_percentage, project_id))
#                                 conn.commit()
#                                 print(f"Project Percentage for ProjectID {project_id} updated to {new_percentage}%.")
#                             else:
#                                 print("Invalid input. Percentage progress must be between 0 and 100.")
#                         else:
#                             print("You are not authorized to update the percentage for this project.")
#
#                     update_description = input(f"Do you want to add or update the task description for ProjectID {project_id}? (yes/no): ").lower()
#                     if update_description == 'yes':
#                         new_description = input(f"Enter new task description for ProjectID {project_id}: ")
#                         project['taskDescription'] = new_description
#                         cursor.execute(f"UPDATE projects SET taskDescription = ? WHERE projectID = ?", (new_description, project_id))
#                         conn.commit()
#                         print(f"Task description for ProjectID {project_id} updated.")
#
#                 else:
#                     print(f"You are not authorized to update ProjectID {project_id}.")
#
#             else:
#                 print(f"Project with ProjectID {project_id} not found or you do not have permission to update.")
#
# # Example usage
# if __name__ == "__main__":
#     db_filename = "wpm_database.db"
#
#     user1 = TeamMembers(
#         userID=1240,
#         user='Miroslava Ezel',
#         role='SuperAdmin',
#         email='n1161732@my.ntu.ac.uk',
#         username='mirkae',
#         password=2309,  # Replace with your actual password
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
#
#
# import sqlite3
# import hashlib
# from prettytable import PrettyTable
#
# class TeamMembers:
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
#     def prompt_for_details(self, entity):
#         details = {}
#         print(f"Enter {entity} details:")
#         for field in ["User", "Role", "Email", "Username", "Password"]:
#             value = input(f"{field}: ")
#             while not value:
#                 print(f"{field} cannot be empty. Please enter a value.")
#                 value = input(f"{field}: ")
#             details[field.lower()] = value
#         return details
#
#     def register_user(self):
#         details = self.prompt_for_details("user")
#
#         hashed_password = self.hash_password(details['password'])
#
#         with sqlite3.connect(self.db_filename) as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 INSERT INTO users (user, role, email, username, password)
#                 VALUES (?, ?, ?, ?, ?)
#             ''', (details['user'], details['role'], details['email'], details['username'], hashed_password))
#             conn.commit()
#             print(f"User {details['username']} registered successfully!")
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
#         def add_project(self, project_name, task, task_description, user, userid, status, percentage, start_date,
#                         end_date):
#             while not all(value.strip() for value in
#                           (project_name, task, task_description, user, userid, status, start_date, end_date)):
#                 print("Project details cannot have empty or whitespace-only values. Please enter all details:")
#                 project_name = input("Project Name: ")
#                 task = input("Task: ")
#                 task_description = input("Task Description: ")
#                 user = input("User: ")
#                 userid = input("UserID: ")
#                 status = input("Status: ")
#                 percentage = input("Percentage: ")
#                 start_date = input("Start Date: ")
#                 end_date = input("End Date: ")
#
#             with sqlite3.connect(self.db_filename) as conn:
#                 cursor = conn.cursor()
#                 cursor.execute('''
#                     INSERT INTO projects (projectName, task, taskDescription, user, userID, role, email, status, percentage, startDate, endDate)
#                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#                 ''', (project_name, task, task_description, user, userid, self.role, self.email, status, percentage,
#                       start_date, end_date))
#                 conn.commit()
#
#     def authorize(self):
#         if self.role == 'SuperAdmin':
#             return True
#         elif self.role == 'Admin':
#             print("You are not authorised to add users or projects.")
#             return False
#         else:
#             print("Invalid role. You do not have authorisation.")
#             return False
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
#         with sqlite3.connect(self.db_filename) as conn:
#             cursor = conn.cursor()
#             cursor.execute("SELECT * FROM projects WHERE projectID = ?", (project_id,))
#             project_data = cursor.fetchone()
#
#             if project_data:
#                 project = dict(zip(self.columns, project_data))
#
#                 if self.role == 'SuperAdmin' or self.userID == project.get('userID'):
#                     print(f"Updating ProjectID {project_id}:")
#
#                     # Display project details
#                     self.display_projects()
#
#                     update_percentage = input(f"Do you want to update the percentage for ProjectID {project_id}? (yes/no): ").lower()
#                     if update_percentage == 'yes':
#                         if self.userID == project.get('userID'):
#                             new_percentage = int(input(f"Enter new percentage status for ProjectID {project_id} (0-100%): "))
#                             if 0 <= new_percentage <= 100:
#                                 project['percentage'] = new_percentage
#                                 cursor.execute(f"UPDATE projects SET percentage = ? WHERE projectID = ?", (new_percentage, project_id))
#                                 conn.commit()
#                                 print(f"Project Percentage for ProjectID {project_id} updated to {new_percentage}%.")
#                             else:
#                                 print("Invalid input. Percentage progress must be between 0 and 100.")
#                         else:
#                             print("You are not authorized to update the percentage for this project.")
#
#                     update_description = input(f"Do you want to add or update the task description for ProjectID {project_id}? (yes/no): ").lower()
#                     if update_description == 'yes':
#                         new_description = input(f"Enter new task description for ProjectID {project_id}: ")
#                         project['taskDescription'] = new_description
#                         cursor.execute(f"UPDATE projects SET taskDescription = ? WHERE projectID = ?", (new_description, project_id))
#                         conn.commit()
#                         print(f"Task description for ProjectID {project_id} updated.")
#
#                 else:
#                     print(f"You are not authorized to update ProjectID {project_id}.")
#
#             else:
#                 print(f"Project with ProjectID {project_id} not found or you do not have permission to update.")
#
# # Example usage
# if __name__ == "__main__":
#     db_filename = "wpm_database.db"
#
#     user1 = TeamMembers(
#         userID=1240,
#         user='Miroslava Ezel',
#         role='SuperAdmin',
#         email='n1161732@my.ntu.ac.uk',
#         username='mirkae',
#         password=2309,  # Replace with your actual password
#         db_filename=db_filename
#     )
#
#     user1.create_tables()
#
#     register_new_user = input("Do you want to register a new user? (yes/no): ").lower()
#     if register_new_user == 'yes' and user1.authorize():
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
#             if add_new_project == 'yes' and user1.authorize():
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

##################################################################################################################### allows none and white spaces
# import sqlite3
# import hashlib
# from prettytable import PrettyTable
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
#
# class TeamMembers:
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
#     def send_email_notification(self, to_email, subject, body):
#         from_email = 'your_email@example.com'  # Replace with your email
#         password = 'your_email_password'  # Replace with your email password
#
#         msg = MIMEMultipart()
#         msg['From'] = from_email
#         msg['To'] = to_email
#         msg['Subject'] = subject
#
#         msg.attach(MIMEText(body, 'plain'))
#
#         with smtplib.SMTP('smtp.example.com', 587) as server:  # Replace with your SMTP server and port
#             server.starttls()
#             server.login(from_email, password)
#             text = msg.as_string()
#             server.sendmail(from_email, to_email, text)
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
#             # Check if the project is complete and send email notification
#             if percentage == 100:
#                 to_email = self.email
#                 subject = f"Project {project_name} Completed!"
#                 body = f"Congratulations! The project '{project_name}' is now complete."
#
#                 self.send_email_notification(to_email, subject, body)
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
#                             # Fetch user email from users table
#                             user_email = cursor.execute("SELECT email FROM users WHERE userID = ?",
#                                                         (project_data[5],)).fetchone()
#                             to_email = user_email[0] if user_email else None
#
#                             if to_email:
#                                 # Send email notification
#                                 subject = f"Project {project['projectName']} Completed!"
#                                 body = f"The project '{project['projectName']}' is now complete."
#
#                                 self.send_email_notification(to_email, subject, body)
#                             else:
#                                 print("User email not found. Email notification not sent.")
#
#                         cursor.execute(f"UPDATE projects SET status = ? WHERE projectID = ?", (new_status, project_id))
#                         conn.commit()
#
#                         print(f"Project Percentage for ProjectID {project_id} updated to {new_percentage}%.")
#                         print(f"Project Status for ProjectID {project_id} updated to {new_status}.")
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
#
# # Example usage
# if __name__ == "__main__":
#     db_filename = "wpm_database.db"
#
#     user1 = TeamMembers(
#         userID=1240,
#         user='Miroslava Ezel',
#         role='SuperAdmin',
#         email='n1161732@my.ntu.ac.uk',
#         username='mirkae',
#         password=2309,  # Replace with your actual password
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
############################################################################################################################################ allows to empty cells, or none values


# import sqlite3
# import hashlib
# from prettytable import PrettyTable
#
#
# class TeamMembers:
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
#
#             # Include 'email' in the SELECT statement
#             cursor.execute(
#                 "SELECT projects.*, users.email FROM projects INNER JOIN users ON projects.userID = users.userID")
#
#             self.projects = [{self.columns[i]: row[i] for i in range(len(self.columns))} for row in cursor.fetchall()]
#
#     def display_projects(self, project_name=None):
#         if self.authenticated:
#             print('Available Projects:')
#             if project_name:
#                 # Adjust the SQL query to include projects that are not 100% complete
#                 query = f"SELECT * FROM projects WHERE projectName = ? AND (percentage < 100 OR percentage IS NULL)"
#                 cursor.execute(query, (project_name,))
#             else:
#                 # Adjust the SQL query to include projects that are not 100% complete
#                 query = "SELECT * FROM projects WHERE percentage < 100 OR percentage IS NULL"
#                 cursor.execute(query)
#
#             self.columns = [col[0] for col in cursor.description]
#             self.projects = [{self.columns[i]: row[i] for i in range(len(self.columns))} for row in cursor.fetchall()]
#
#             # Print Database Column Names
#             print("Database Column Names:", self.columns)
#
#             table = PrettyTable(self.columns)
#             for project in self.projects:
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
#                         print(f"Project Percentage for ProjectID {project_id} updated to {new_percentage}%.")
#                         print(f"Project Status for ProjectID {project_id} updated to {new_status}.")
#
#                         # Send email notification
#                         to_email = project.get('email')
#                         if to_email:
#                             subject = f"Project {project.get('projectName')} Completed!"
#                             body = f"Dear {project.get('user')},\n\nYour project {project.get('projectName')} is now complete!\n\nBest regards,\nThe Project Management Team"
#                             send_email(to_email, subject, body)
#
#                             print(f"Email notification sent to {to_email}.")
#                         else:
#                             print("Email notification not sent. User email not found.")
#
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
#
# # Function to send email notification
# def send_email(to_email, subject, body):
#     # Replace with your email sending code or library
#     # For example, you can use the 'smtplib' library in Python to send emails
#     # Here's a simple example (replace placeholders with actual email server details):
#     import smtplib
#     from email.mime.text import MIMEText
#     from email.mime.multipart import MIMEMultipart
#
#     smtp_server = "smtp.gmail.com"
#     smtp_port = 587
#     smtp_username = "xxxxxxxxxxxxxxxx"
#     smtp_password = "xxxxxxxxxxxx"
#
#     sender_email = "n1161732@my.ntu.ac.uk"
#
#     message = MIMEMultipart()
#     message['From'] = sender_email
#     message['To'] = to_email
#     message['Subject'] = subject
#     message.attach(MIMEText(body, 'plain'))
#
#     try:
#         with smtplib.SMTP(smtp_server, smtp_port) as server:
#             server.starttls()
#             server.login(smtp_username, smtp_password)
#             server.sendmail(sender_email, to_email, message.as_string())
#
#         print(f"Email notification sent to {to_email}.")
#     except Exception as e:
#         print(f"Error sending email: {e}")
#
# # Example usage
# to_email = "n@my.ntu.ac.uk"  # Replace with your actual email
# subject = "Test Subject"
# body = "This is a test email body."
# send_email(to_email, subject, body)
#
# # Example usage
# if __name__ == "__main__":
#     db_filename = "wpm_database.db"
#
#     user1 = TeamMembers(
#         userID=1240,
#         user='Miroslava Ezel',
#         role='SuperAdmin',
#         email='n1161732@my.ntu.ac.uk',  # Replace with your actual email
#         username='mirkae',
#         password=2309,  # Replace with your actual password
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
#                 user1.add_project(project_name, task, task_description, user, userid, status, percentage, start_date,
#                                   end_date)
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

#################################################################################################################### email simulaton, allows empty cells
# import sqlite3
# import hashlib
# from prettytable import PrettyTable
#
# class TeamMembers:
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
#     def send_email(self, to_email, subject, body):
#         print(f"Simulating email notification to: {to_email}")
#         print(f"Subject: {subject}")
#         print(f"Body: {body}")
#
#     def send_and_display_notification(self, to_email, subject, body):
#         self.send_email(to_email, subject, body)
#         print(f"Email notification sent to {to_email}.")
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
#                         new_status = "Not Started"
#                         if new_percentage > 0:
#                             new_status = "In Progress"
#                         if new_percentage == 100:
#                             new_status = "Complete"
#
#                         cursor.execute(f"UPDATE projects SET status = ? WHERE projectID = ?", (new_status, project_id))
#                         conn.commit()
#
#                         print(f"Project Percentage for ProjectID {project_id} updated to {new_percentage}%.")
#                         print(f"Project Status for ProjectID {project_id} updated to {new_status}.")
#
#                         to_email = project.get('email', '')  # Replace with the actual email column name
#                         subject = f"Project {project_id} Completed"
#                         body = f"Project {project_id} has been completed. Congratulations!"
#                         self.send_and_display_notification(to_email, subject, body)
#                         print("Email notification sent.")
#
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
# # Example usage
# if __name__ == "__main__":
#     db_filename = "wpm_database.db"
#
#     user1 = TeamMembers(
#         userID=1240,
#         user='Miroslava Ezel',
#         role='SuperAdmin',
#         email='n1161732@my.ntu.ac.uk',
#         username='mirkae',
#         password=2309,  # Replace with your actual password
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
#         username_input = input('Enter your username: ')
#         password_input = input('Enter your password: ')
#
#         if user1.login(username_input, password_input):
#             print("Login successful.")
#
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

######################################          email simulation - works but sends notification even if it is not 100  ########################################

# import sqlite3
# import hashlib
# from prettytable import PrettyTable
#
# class TeamMembers:
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
#                         # Send email notification
#                         subject = f"Project {project_id} Completed"
#                         body = f"Congratulations! The project {project_id} has been completed."
#
#                         self.send_and_display_notification(project_id, subject, body)
#
#                         print(f"Project Percentage for ProjectID {project_id} updated to {new_percentage}%.")
#                         print(f"Project Status for ProjectID {project_id} updated to {new_status}.")
#                         print(f"Email notification sent to the user.")
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
#     user1 = TeamMembers(
#         userID=1240,
#         user='Miroslava Ezel',
#         role='SuperAdmin',
#         email='n1161732@my.ntu.ac.uk',
#         username='mirkae',
#         password=2309,  # Replace with your actual password
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

################################  email simulation - this works perfect in all aspects, but allows empty spaces and move to next question #########################################################


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
        if any(val is None or val.strip() == "" for val in
               (project_name, task, task_description, user, userid, status, start_date, end_date)):
            print("Project details cannot have None values or be empty. Please enter all details.")
            return

        if percentage is None or not (0 <= percentage <= 100):
            print("Percentage must be between 0 and 100.")
            return

        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO projects (projectName, task, taskDescription, user, userID, role, email, status, percentage, startDate, endDate)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
            project_name, task, task_description, user, userid, self.role, self.email, status, percentage, start_date,
            end_date))
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

                        if new_percentage == 100:
                            # Send email notification
                            subject = f"Project {project_id} Completed"
                            body = f"The project {project_id} has been completed."

                            self.send_and_display_notification(project_id, subject, body)

                            print(f"Project Percentage for ProjectID {project_id} updated to {new_percentage}%.")
                            print(f"Project Status for ProjectID {project_id} updated to {new_status}.")
                            print(f"Email notification sent to the user.")
                        else:
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

            else:
                print(f"Project with ProjectID {project_id} not found.")

    def send_email(self, to_email, subject, body):
        print(f"Simulating email notification to: {to_email}")
        print(f"Subject: {subject}")
        print(f"Body: {body}")

    def send_and_display_notification(self, project_id, subject, body):
        user_email = self.get_user_email(project_id)

        if user_email:
            self.send_email(user_email, subject, body)
            print(f"Email notification sent to {user_email}.")
            print(f"Email notification sent to SuperAdmin.")
        else:
            print("User email not found. Email notification not sent.")

    def get_user_email(self, project_id):
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            user_email = cursor.execute("SELECT email FROM projects WHERE projectID = ?", (project_id,)).fetchone()

        return user_email[0] if user_email else None


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

            user1.load_projects_from_db()
            user1.display_projects()
            login_success = True
        else:
            print("Login failed. Please check your username and password.")
