import unittest
from WMS_submit import SuperAdmin, AddProject

class TestSuperAdmin(unittest.TestCase):
    def setUp(self):
        # This method is called before each test
        self.superadmin = SuperAdmin(
            userID=9,
            user='Tom Becker',
            role='SuperAdmin',
            email='n1161732@my.ntu.ac.uk',
            username='tomb',
            password=123,
            db_filename='wpm_database.db'
        )

    def test_fetch_projects(self):

        projects = self.superadmin.fetch_projects()
        self.assertIsInstance(projects, list, "Fetch projects should return a list")

    def test_add_project(self):
        # add_project method is present in SuperAdmin class
        projectName = "Loans"
        task = "5"
        taskDescription = "Interest Review"
        user = "Tom Becker"
        userID = "9"
        email = "n1161732@my.ntu.ac.uk"
        status = "In Progress"
        percentage = 35
        startDate = "01/01/2024"
        endDate = "01/02/2024"

        result = self.superadmin.add_project(
            projectName, task, taskDescription, user, userID, email, status, percentage, startDate, endDate
        )

        #self.assertTrue(result, "Adding a project should return True on success")
        self.assertFalse(result, "Adding a project should return False if not authorized or unsuccessful")

    # More test methods can be added for other SuperAdmin functionalities

if __name__ == '__main__':
    unittest.main()

class TestAddProject(unittest.TestCase):
    def setUp(self):
        # This method is called before each test
        self.add_project_instance = AddProject(
            db_filename='wpm_database.db',
            role='SuperAdmin',
            email='n1161732@my.ntu.ac.uk'
        )

    def test_add_project(self):
        projectName = "Loans"
        task = "5"
        taskDescription = "Interest Review"
        user = "Tom Becker"
        userID = "9"
        email = "n1161732@ntu.ac.uk"
        status = "In Progress"
        percentage = 35
        startDate = "01/01/2024"
        endDate = "01/02/2024"

        result = self.add_project_instance.execute(
            projectName, task, taskDescription, user, userID, status, percentage, startDate, endDate
        )

        self.assertTrue(result, "Adding a project should return True on success")

if __name__ == '__main__':
    unittest.main()