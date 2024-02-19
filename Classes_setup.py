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
        #print(f"Loading projects from database: {self.db_filename}")
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM projects")
            self.columns = [col[0] for col in cursor.description]
            self.projects = [{self.columns[i]: row[i] for i in range(len(self.columns))} for row in cursor.fetchall()]

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
            self.view_users()

class ViewExistingProject:
    def __init__(self, db_filename):
        self.db_filename = db_filename

    def view_existing_project(self):
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT projectID, projectName, taskDescription, user, userID, role, email, status, percentage, startDate, endDate FROM projects")
            user_data = cursor.fetchall()

            if not user_data:
                print("No projects found.")
                return

            columns = ["projectID", "projectName", "taskDescription", "user", "userID", "role", "email", "status", "percentage", "starDate", "endDate"]
            table = PrettyTable(columns)
            for user_data in user_data:
                table.add_row(user_data)

            print("Logged Projects in progress:")
            print(table)

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
        #print(f"Loading projects from database: {self.db_filename}")
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
                new_value = input(f"Enter new value for {col}: ").strip() # updates the Percentage column
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

               # print(f"Project Percentage for ProjectID {project_id} updated to {new_percentage}%.")
               # print(f"Project Status for ProjectID {project_id} updated to {new_status}.") # removed the automatically

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

       # print("SuperAdmin loading projects from the database.")
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

        # # Set the role attribute after registering the user
        # self.role = cursor.execute("SELECT role FROM users WHERE username = ?", (self.username,)).fetchone()[0]

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

         # Create an instance of SendEmail
        self.send_email_instance = SendEmail(db_filename)

    def update_project(self, project_id):
        # Your implementation of update_project for SuperAdmin
        print(f"Updating project: {project_id}")

        self.send_email_instance.send_and_display_notification(project_id, subject, body)

    def update_existing_user(self):
        # Call the parent class method
        super().update_existing_user()


# Example usage
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

    login_success = False

    while not login_success:
        # Login Simulation
        username_input = input('Enter your username: ')
        password_input = input('Enter your password: ')

        if user1.login(username_input, password_input):
            print("Login successful.")

            # View registered users
            view_users_option = input("Do you want to view all registered users? (yes/no): ").lower()
            if view_users_option == 'yes':
                if user1.role == 'SuperAdmin':
                    view_handler = ViewUsers(db_filename)
                    view_handler.view_users()
                else:
                    user1.view_users()

            register_new_user = input("Do you want to register a new user? (yes/no): ").lower()
            if register_new_user == 'yes':
                user1.register_user()

            # Update existing user
            update_existing_user_option = input("Do you want to update an existing user? (yes/no): ").lower()
            if update_existing_user_option == 'yes':
                if user1.role == 'SuperAdmin':
                    update_handler = UpdateExistingUsers(db_filename)
                    update_handler.update_existing_user()
                else:
                    print("You are not authorized to update users.")

            # View existing projects
            view_existing_project_option = input("Do you want to view all projects? (yes/no): ").lower()
            if view_existing_project_option == 'yes':
                if user1.role == 'SuperAdmin':
                    view_handler = ViewExistingProject(db_filename)
                    view_handler.view_existing_project()
                else:
                    user1.view_existing_projects()



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

                user1.add_project(project_name, task, task_description, user, userid, email, status, percentage, start_date,
                                  end_date)

                print(f"Project '{project_name}' created successfully!")


            # Create an instance of UpdateProject
            update_project_instance = UpdateProject(user1, db_filename)

            update_existing_project = input("Do you want to update an existing project? (yes/no): ").lower()
            if update_existing_project == 'yes':
                # Display available projects
                user1.load_projects_from_db()
                user1.display_projects()

                project_id_to_update = input("Enter the ProjectID you want to update: ")
                update_project_instance.update_project(project_id_to_update)

            user1.load_projects_from_db()
            user1.display_projects()
            login_success = True
        else:
            print("Login failed. Please check your username and password.")

    send_email_instance = SendEmail(db_filename)
    update_project_instance = UpdateProject(send_email_instance, db_filename)

    # Create an instance of UpdateProject
    update_project_instance = UpdateProject(user1, db_filename)

