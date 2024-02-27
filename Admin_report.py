import sqlite3
import hashlib
from prettytable import PrettyTable


class Login:
    def __init__(self, db_filename):
        self.db_filename = db_filename
        self.authenticated = False
        self.userID = None
        self.user = None
        self.role = None
        self.email = None
        self.username = None

    def hash_password(self, password):
        return hashlib.sha256(str(password).encode()).hexdigest()

    def validate_input(self, prompt, allow_empty=False):
        while True:
            user_input = input(prompt).strip()
            if allow_empty or user_input:
                return user_input
            else:
                print("Input cannot be empty. Please enter a value.")

    # def login(self, enter_username, enter_password):
    #     hashed_password = self.hash_password(enter_password)
    #
    #     with sqlite3.connect(self.db_filename) as conn:
    #         cursor = conn.cursor()
    #         cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (enter_username, hashed_password))
    #
    #         user_data = cursor.fetchone()
    #
    #     if user_data:
    #         self.authenticated = True
    #         self.userID = user_data[0]
    #         self.user = user_data[1]
    #         self.role = user_data[2]
    #         self.email = user_data[3]
    #         self.username = user_data[4]
    #         return True
    #     else:
    #         return False
    def login(self, enter_username, enter_password):
        self.login_username = enter_username
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
            print(f"Welcome, {self.username}!")
            print(f"Logged in as: UserID={self.userID}, Username={self.username}")
            return True
        else:
            self.authenticated = False
            print("Login failed. Please check your username and password.")
            return False


class WorkManagementSystem:
    def __init__(self, db_filename):
        self.db_filename = db_filename
        self.login_instance = None
        self.team_members_instance = None
        self.superadmin_instance = None

    def start(self):
        print("Welcome to the Work Management System!")
        db_initialized = self.initialize_database()

        if db_initialized:
            self.login_instance = Login(self.db_filename)

            # Obtain username and password from the user
            enter_username = input("Enter your username: ")
            enter_password = input("Enter your password: ")

            logged_in = self.login_instance.login(enter_username, enter_password)

            if logged_in:
                self.team_members_instance = TeamMembers(
                    self.login_instance.userID,
                    self.login_instance.user,
                    self.login_instance.role,
                    self.login_instance.email,
                    self.login_instance.username,
                    self.login_instance.hash_password(enter_password),
                    self.db_filename  # pass db_filename to TeamMembers constructor
                )

                if self.team_members_instance.role == "SuperAdmin":
                    self.superadmin_instance = SuperAdmin(self.login_instance.userID,
                                                          self.login_instance.user,
                                                          self.login_instance.role,
                                                          self.login_instance.email,
                                                          self.login_instance.username,
                                                          self.login_instance.hash_password(enter_password),
                                                          self.db_filename)

                #self.menu()

    def initialize_database(self):
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

            return True


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
        view_handler = ViewExistingProject(self.db_filename)
        view_handler.view_existing_project()

    def load_projects_from_db(self):
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM projects")
            self.columns = [col[0] for col in cursor.description]
            self.projects = [{self.columns[i]: row[i] for i in range(len(self.columns))} for row in cursor.fetchall()]

    def is_project_owner(self, project_id):
        """
        Check if the logged-in user is the owner of the project.

        :param project_id: ProjectID to check
        :return: True if the user is the owner, False otherwise
        """
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT userID FROM projects WHERE projectID = ?", (project_id,))
            owner_id = cursor.fetchone()

            # Check if the logged-in user's ID matches the owner ID
            return owner_id == self.userID

    def view_assigned_projects(self):
        try:
            # Debugging statement
            print(f"Debug: UserID in view_assigned_projects: {self.userID}")

            # Fetch projects based on the userID
            query = f"SELECT * FROM projects WHERE userID = {self.userID}"

            # Print the exact SQL query
            print(f"Debug: Executing query: {query}")

            projects = self.execute_query(query)

            # Debugging statement
            print(f"Debug: Fetched projects (raw): {projects}")

            if not projects:
                print("No projects assigned.")
            else:
                print("Assigned Projects:")
                columns = projects[0].keys()
                table = PrettyTable(columns)

                for project in projects:
                    table.add_row([project[col] for col in columns])

                print(table)

        except Exception as e:
            print(f"An error occurred: {e}")


    def display_projects(self, project_name=None):
        if self.authenticated:
            print('Available Projects:')
            if project_name:
                projects_to_display = [project for project in self.projects if
                                       project.get('projectName') == project_name]
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

    def execute_query(self, query):
        """
        Execute a SQL query and return the results.

        :param query: SQL query to execute
        :return: Results of the query
        """
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
        return result

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


class UpdateExistingUsers:
    def __init__(self, db_filename):
        self.db_filename = db_filename

    def update_existing_user(self):

        while True:
            user_id_to_update = input("Enter the UserID of the user you want to update: ")
            user_to_update = input("Enter the username of the user you want to update:")

            with sqlite3.connect(self.db_filename) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE userID = ? AND user = ?", (user_id_to_update, user_to_update))
                user_data = cursor.fetchone()

                if not user_data:
                    print(f"User with UserID {user_id_to_update}, username {user_to_update} role {user_to_update} and email {user_to_update} not found.")
                    break

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
                    cursor.execute(f"UPDATE users SET {col} = ? WHERE userID = ? AND user = ?",
                                   (new_value, user_id_to_update, user_to_update))
                    conn.commit()

                print(f"User details for UserID {user_id_to_update}, username {user_to_update}, role {user_to_update}, email {user_to_update} updated successfully.")

            update_more_users = input("Do you want to update more users? (yes/no): ").lower()
            if update_more_users != 'yes':
                break


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
                    INSERT INTO users (User, role, email, username, password)
                    VALUES (?, ?, ?, ?, ?)
                ''', (user, role, email, username, hashed_password))
                conn.commit()

            print(f"User {user} registered successfully!")

            # Ask if the user wants to add more users after completing other operations
            add_more_users = input("Do you want to add more users? (Y/N): ").lower()
            if add_more_users != 'y':
                break

            # Display the updated user table
            view_users_instance = ViewUsers(self.db_filename)
            view_users_instance.view_users()


class ViewExistingProject:
    def __init__(self, db_filename):
        self.db_filename = db_filename

    def view_existing_project(self):
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT projectID, projectName, task, taskDescription, user, userID, role, email, status, percentage, startDate, endDate FROM projects")
            user_data = cursor.fetchall()

            if not user_data:
                print("No projects found.")
                return

            columns = ["projectID", "projectName", "task", "taskDescription", "user", "userID", "role", "email", "status", "percentage", "startDate", "endDate"]
            table = PrettyTable(columns)
            for user_data in user_data:
                table.add_row(user_data)

            print("Logged Projects in progress:")
            print(table)

    def get_project_details(self, project_id):
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM projects WHERE projectID = ?", (project_id,))
            project_details = cursor.fetchone()

            return project_details

class AddProject:
    def __init__(self, db_filename, role, email):
        self.db_filename = db_filename
        self.role = role
        self.email = email

    def validate_percentage(self, percentage):
        return percentage.isdigit() and 0 <= int(percentage) <= 100

    def execute(self, projectname, task, taskdescription, user, userid, status, percentage, startDate, endDate):
        print("Enter project details:")

        if not self.validate_percentage(percentage):
            print("Invalid input. Percentage progress must be an integer between 0 and 100.")
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




class UpdateProject:
    def __init__(self, user_instance, db_filename):
        self.user_instance = user_instance
        self.db_filename = db_filename

    def update_project(self, project_id):
        if not self.user_instance.authenticated or self.user_instance.role != 'SuperAdmin':
            print("You are not authorized to update projects.")
            return

        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM projects WHERE projectID = ?", (project_id,))
            project_data = cursor.fetchone()

            if not project_data:
                print(f"Project with ProjectID {project_id} not found.")
                return

            project_columns = [col[0] for col in cursor.description]
            project = dict(zip(project_columns, project_data))

            # Display project details before updating multiple columns
            columns_to_display = project_columns
            table_to_display = PrettyTable(columns_to_display)
            table_to_display.add_row([project.get(col, '') for col in columns_to_display])
            print("Project details before update:")
            print(table_to_display)

            # Input multiple columns to update
            columns_to_update = input("Enter the columns you want to update (comma-separated): ").split(',')
            columns_to_update = [col.strip() for col in columns_to_update]

            for col in columns_to_update:
                if col not in project_columns:
                    print(f"Invalid column '{col}'. Please choose from {', '.join(project_columns)}")
                    return
            for col in columns_to_update:
                new_value = input(f"Enter new value for {col}: ").strip()  # updates the Percentage column
                cursor.execute(f"UPDATE projects SET {col} = ? WHERE projectID = ?", (new_value, project_id))
                conn.commit()

            # Update status based on percentage
            new_percentage = int(input(f"Please confirm the percentage for ProjectID {project_id} (0-100%): "))
            if 0 <= new_percentage <= 100:
                new_status = "Not Started" if new_percentage == 0 else "In Progress" if new_percentage < 100 else "Complete"
                cursor.execute("""
                        UPDATE projects 
                        SET percentage = ?, 
                            status = ? 
                        WHERE projectID = ?
                    """, (new_percentage, new_status, project_id))

                conn.commit()

                if new_status == 'Complete':
                    # Send email notification
                    subject = f"Project {project_id} Completed"
                    body = f"The project {project_id} has been completed."

                    self.user_instance.send_and_display_notification(project_id, subject, body)

                    print(f"Project Percentage for ProjectID {project_id} updated to {new_percentage}%.")
                    print(f"Project Status for ProjectID {project_id} updated to {new_status}.")
                    print(f"Email notification sent to the user.")
                else:
                    print(f"Project Percentage for ProjectID {project_id} updated to {new_percentage}%.")
                    print(f"Project Status for ProjectID {project_id} updated to {new_status}.")
            else:
                print("Invalid input. Percentage progress must be between 0 and 100.")

            # Display the updated project details
            cursor.execute("SELECT * FROM projects WHERE projectID = ?", (project_id,))
            updated_project_data = cursor.fetchone()
            updated_project = dict(zip(project_columns, updated_project_data))
            print("Project details after update:")
            table_to_display = PrettyTable(project_columns)
            table_to_display.add_row([updated_project.get(col, '') for col in project_columns])
            print(table_to_display)

            print(f"Project details for ProjectID {project_id} updated successfully.")

class SendEmail:
    def __init__(self, db_filename):
        self.db_filename = db_filename

    def send_and_display_notification(self, project_id, subject, body):
        user_email = self.get_user_email(project_id)

        if user_email:
            # Check if the percentage is 100
            if self.check_percentage_100(project_id):
                self.send_email(user_email, subject, body)
                print(f"Email notification sent to {user_email}.")
                print(f"Email notification sent to SuperAdmin.")
            else:
                print("Percentage is not 100. Email notification not sent.")
        else:
            print("User email not found. Email notification not sent.")

    def get_user_email(self, project_id):
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            user_email = cursor.execute("SELECT email FROM projects WHERE projectID = ?", (project_id,)).fetchone()

        return user_email[0] if user_email else None

    def check_percentage_100(self, project_id):
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            percentage = cursor.execute("SELECT percentage FROM projects WHERE projectID = ?", (project_id,)).fetchone()

        return percentage[0] == 100 if percentage else False

    def send_email(self, to_email, subject, body):
        # Original send_email functionality
        # print(f"Simulating email notification to: {to_email}")
        print(f"Subject: {subject}")
        print(f"Body: {body}")


class SuperAdmin(TeamMembers, Login, SendEmail):
    def __init__(self, userID, user, role, email, username, password, db_filename):
        super().__init__(userID, user, role, email, username, password, db_filename)

    def load_projects_from_db(self):
        super().load_projects_from_db()

    # Override the register_user method to allow SuperAdmin to create new users
    def register_user(self):
        print("Enter user details:")
        self.user = self.validate_input("User: ")
        self.role = self.validate_input("Role: ")
        self.email = self.validate_input("Email: ")
        self.username = self.validate_input("Username: ")
        self.password = self.validate_input("Password: ")

        hashed_password = self.hash_password(self.password)

        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (User, role, email, username, password)
                VALUES (?, ?, ?, ?, ?)
            ''', (self.user, self.role, self.email, self.username, hashed_password))
            conn.commit()

        print(f"User {self.user} registered successfully!")

    # Override the add_project method to allow SuperAdmin to create new projects
    def add_project(self, project_name, task, task_description, user, userid, email, status, percentage, start_date, end_date):
        while True:
            if not self.authenticated or self.role != 'SuperAdmin':
                print("You are not authorised to create a new project.")
                break

            print("Enter project details:")

            if not (percentage.isdigit() and 0 <= int(percentage) <= 100):
                print("Invalid input. Percentage progress must be an integer between 0 and 100.")
                break

            with sqlite3.connect(self.db_filename) as conn:
                cursor = conn.cursor()

                # Fetch the user's role from the database
                user_data = cursor.execute("SELECT role, email FROM users WHERE userID = ?", (userid,)).fetchone()

                if user_data:
                    user_role, user_email = user_data
                else:
                    print(f"User with UserID {userid} not found.")
                    break
                cursor.execute('''
                             INSERT INTO projects (projectName, task, taskDescription, user, userID, role, email, status, percentage, startDate, endDate)
                                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (project_name, task, task_description, user, userid, user_role, user_email, status, percentage,
                              start_date, end_date))
                conn.commit()

            print(f"Project '{project_name}' created successfully!")

            add_more_projects = input("Do you want to add more projects? (y/n): ").lower()
            if add_more_projects != 'y':
                break



    def update_project(self, project_id):
        # Your implementation of update_project for SuperAdmin
        print(f"Updating project: {project_id}")





    def update_existing_user(self):
        # Call the parent class method
        super().update_existing_user()

class Admin(Login, SendEmail):
    def __init__(self, userID, user, role, email, username, password, db_filename):


        self.userID = userID
        self.user = user
        self.role = role
        self.email = email
        self.username = username
        self.password = password
        self.authenticated = False
        self.db_filename = db_filename
        # self.columns = []  # To store column names
        # self.projects = []

    def load_projects_from_db(self):
        super().load_projects_from_db()

    def admin_menu(self):
        # Admin-specific menu with limited options
        print("Admin Options:")
        print("1. Send Email")
        print("2. View Existing Projects and Write Report")
        print("3. Logout")

    def admin_actions(self, option):
        if option == '1':
            # Send Email
            to_email = input("Enter recipient's email address: ")
            subject = input("Enter email subject: ")
            body = input("Enter email body: ")
            self.send_email(to_email, subject, body)

        elif option == '2':
            # View Existing Projects and Write Report
            view_existing_project_option = input("Do you want to view all projects? (yes/no): ").lower()
            if view_existing_project_option == 'yes':
                view_handler = ViewExistingProject(self.db_filename)
                view_handler.view_existing_project()

            # Write Report
            project_id = input("Enter the ProjectID for which you want to write a report: ")
            self.generate_project_report(project_id)

            # Additional code for writing a report to a text file
            write_report_option = input("Do you want to write a report? (yes/no): ").lower()
            if write_report_option == 'yes':
                to_email = input("Enter recipient's email address: ")
                subject = input("Enter email subject: ")
                body = input("Enter email body: ")

                # Retrieve project details using the appropriate method in ViewExistingProject
                project_details = self.get_project_details(project_id)

                if project_details:
                    # Generate and store the report as a text file
                    report_content = f"Project Report for ProjectID: {project_id}\n\n"
                    for column, value in project_details.items():
                        report_content += f"{column}: {value}\n"
                    report_content += f"\nReport Body:\n{body}"

                    report_filename = f"ProjectReport_{project_id}.txt"

                    with open(report_filename, 'w') as report_file:
                        report_file.write(report_content)

                    print(f"Report generated and saved as {report_filename}")
                else:
                    print(f"Project with ProjectID {project_id} not found.")




        elif option == '3':
            print("Logging out.")
            return True  # Signal to logout

        else:
            print("Invalid option. Please enter a number between 1 and 3.")

        return False  # Continue with the menu

    def login_menu(self):
        # Override login menu to provide Admin-specific menu
        print("Login Options:")
        print("1. Login")
        print("2. Exit")

    def execute_query(self, query):
        try:
            connection = sqlite3.connect(self.db_filename)
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            connection.commit()
            return result
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            if connection:
                connection.close()

    def get_project_details(self, project_id):
        # Replace this with your actual database query
        query = f"SELECT projectID, projectName, task, taskDescription, user, userID, role, email, status, percentage, startDate, endDate FROM projects WHERE projectID = {project_id}"


        # Use self.execute_query(query) to execute the query
        project_details = self.execute_query(query)

        # Check if project_details is not empty (adjust this based on your database interaction)
        if project_details:
            # Assuming the query fetches only one project, convert it to a dictionary
            columns = ["projectID", "projectName", "task", "taskDescription", "user", "userID", "role", "email",
                       "status", "percentage", "startDate", "endDate"]
            project_dict = dict(zip(columns, project_details[0]))

            return project_dict
        else:
            return None

    #

    def generate_project_report(self, project_id):
        project_details = self.get_project_details(project_id)

        if project_details:
            # Display project details using PrettyTable
            columns = list(project_details.keys())
            table_to_display = PrettyTable(columns)

            # Add a single row with project details
            table_to_display.add_row([project_details[col] for col in columns])

            print(table_to_display)
        else:
            print(f"Project with ProjectID {project_id} not found.")

    #
    def get_project_columns(self):
        # Retrieve column names from the projects table
        query = "PRAGMA table_info(projects)"
        columns_info = self.execute_query(query)

        if columns_info:
            # Extract column names from the result
            column_names = [column[1] for column in columns_info]
            return column_names
        else:
            return None


if __name__ == "__main__":
    db_filename = "wpm_database.db"
    project_management_system = WorkManagementSystem(db_filename)

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

    # Login simulation loop
    login_success = False

    while not login_success:
        # Login Simulation
        username_input = input('Enter your username: ')
        password_input = str(input('Enter your password: '))

        if user1.login(username_input, password_input):
            print(f"Welcome, {username_input}!")
            print(f"Logged in as: UserID={user1.userID}, Username={user1.username}")
            print("Login successful.")

            if user1.role == 'Admin':
                admin_user = Admin(
                    userID=user1.userID,
                    user=user1.user,
                    role=user1.role,
                    email=user1.email,
                    username=user1.username,
                    password=user1.password,
                    db_filename=db_filename
                )
                while True:
                    admin_user.admin_menu()
                    option_admin = input("Enter your choice (1-3): ")
                    logout = admin_user.admin_actions(option_admin)
                    if logout:
                        break  # Logout and go back to the main login menu



            elif user1.role == 'SuperAdmin':
                # Continue with SuperAdmin actions
                while True:
                    # SuperAdmin section
                    print("Options:")
                    print("1. View registered users")
                    print("2. Register a new user")
                    print("3. Update an existing user")
                    print("4. View existing projects")
                    print("5. Add or update a project")
                    print("6. Close the script")

                    option_superadmin = input("Enter your choice (1-6): ")

                    if option_superadmin == '1':
                        # View registered users
                        view_users_option = input("Do you want to view all registered users? (yes/no): ").lower()
                        if view_users_option == 'yes':
                            if user1.role == 'SuperAdmin':
                                view_handler = ViewUsers(db_filename)
                                view_handler.view_users()
                            else:
                                user1.view_users()

                    elif option_superadmin == '2':
                        # Register new user
                        register_new_user = input("Do you want to register a new user? (yes/no): ").lower()
                        if register_new_user == 'yes':
                            user1.register_user()

                    elif option_superadmin == '3':
                        # Update existing user
                        update_existing_user_option = input(
                            "Do you want to update an existing user? (yes/no): ").lower()
                        if update_existing_user_option == 'yes':
                            if user1.role == 'SuperAdmin':
                                update_handler = UpdateExistingUsers(db_filename)
                                update_handler.update_existing_user()
                            else:
                                print("You are not authorized to update users.")

                    elif option_superadmin == '4':
                        # View existing projects
                        view_existing_project_option = input("Do you want to view all projects? (yes/no): ").lower()
                        if view_existing_project_option == 'yes':
                            if user1.role == 'SuperAdmin':
                                view_handler = ViewExistingProject(db_filename)
                                view_handler.view_existing_project()
                            else:
                                user1.view_existing_projects()

                    elif option_superadmin == '5':
                        # Adding or Updating a project
                        add_project = input("Do you want to add a new project? (yes/no): ").lower()
                        if add_project == 'yes':
                            # View existing projects before adding a new one
                            user1.view_existing_projects()

                            project_name = input("Enter project name: ")
                            task = input("Enter task: ")
                            task_description = input("Enter task description: ")
                            user = input("Enter user: ")
                            userid = input("Enter UserID: ")
                            email = input("Enter email: ")

                            status = input("Enter status: ")
                            percentage = input("Enter percentage: ")
                            start_date = input("Enter start date: ")
                            end_date = input("Enter end date: ")

                            user1.add_project(project_name, task, task_description, user, userid, email, status,
                                              percentage,
                                              start_date, end_date)

                            print(f"Project '{project_name}' created successfully!")

                        # Create an instance of UpdateProject
                        update_project_instance = UpdateProject(user1, db_filename)

                        # Update an existing project
                        update_existing_project = input("Do you want to update an existing project? (yes/no): ").lower()
                        if update_existing_project == 'yes':
                            # Display available projects
                            user1.load_projects_from_db()
                            user1.display_projects()

                            project_id_to_update = input("Enter the ProjectID you want to update: ")
                            update_project_instance.update_project(project_id_to_update)

                        user1.load_projects_from_db()
                        user1.display_projects()

                    elif option_superadmin == '6':
                        print('Closing the system')
                        login_success = True
                        break  # Exit the inner loop
                    else:
                        print("Invalid option. Please enter a number between 1 and 6.")
                    pass


            elif user1.role == 'TeamMember':
                # Continue with TeamMember actions
                while True:
                    # TeamMember section
                    print("Options:")
                    print("1. View assigned projects")
                    print("2. View existing projects")
                    print("3. Update project")
                    print("4. View existing users")
                    print("5. Close the script")

                    option_teammember = input("Enter your choice (1-5): ")

                    if option_teammember == '1':
                        # Fetch projects based on the entered userID
                        query = f"SELECT * FROM projects WHERE userID = {user1.userID}"
                        # print(f"Debug: Executing query: {query}")
                        projects = user1.execute_query(query)

                        if projects:
                            print(f"Assigned Projects for UserID {user1.userID}:")
                            columns_to_display = ["projectID", "projectName", "task", "taskDescription", "status",
                                                  "percentage", "startDate", "endDate"]
                            table_to_display = PrettyTable(columns_to_display)

                            for project in projects:
                                table_to_display.add_row(
                                    [project[0], project[1], project[2], project[3], project[8], project[9],
                                     project[10], project[11]])

                            print(table_to_display)
                        else:
                            print(f"No projects assigned for UserID {user1.userID}")

                    elif option_teammember == '2':
                        view_existing_project_option = input("Do you want to view all projects? (yes/no): ").lower()
                        if view_existing_project_option == 'yes':
                            view_handler = ViewExistingProject(db_filename)
                            view_handler.view_existing_project()

                    elif option_teammember == '3':
                        project_id_to_update = input("Enter the ProjectID you want to update: ")

                        # Check if the logged-in user is the owner of the project
                        if user1.is_project_owner(project_id_to_update):
                            update_project_instance = UpdateProject(user1, db_filename)
                            update_project_instance.update_project(project_id_to_update)
                        else:
                            print("You are not authorized to update this project.")

                    elif option_teammember == '4':
                        # View existing users
                        view_users_instance = ViewUsers(db_filename)
                        view_users_instance.view_users()

                    elif option_teammember == '5':
                        print('Closing the system')
                        break
                    else:
                        print("Invalid option. Please enter a number between 1 and 5.")
                    pass
        else:
            print("Login failed. Please try again.")
