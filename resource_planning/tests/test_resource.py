from datetime import datetime, timedelta
from odoo import exceptions
from odoo.tests import common
from psycopg2 import errors


class TestResource(common.TransactionCase):
    """
    Class to test the Resource class
    """

    def test_compute_weeks_normal(self):
        """
        Tests if the returned array from the compute_weeks method contains the correct weeks
        (multiple weeks)

        """
        start_date = datetime(2020, 4, 5, 23, 55, 0)
        end_date = datetime(2020, 4, 14, 12, 42, 7)

        week_data = self.env['resource.model'].compute_weeks(start_date, end_date)

        self.assertEqual(
            week_data[1],
            [{'week_num': 14, 'year': 2020}, {'week_num': 15, 'year': 2020}, {'week_num': 16, 'year': 2020}],
            'Should calculate project weeks 14 to 16'
        )

    def test_compute_weeks_normal_over_year_bound(self):
        """
        Tests if compute_weeks works correctly at a turn of the year

        """
        start_date = datetime(2019, 12, 27, 0, 0, 0)
        end_date = datetime(2020, 1, 17, 7, 30, 25)

        week_data = self.env['resource.model'].compute_weeks(start_date, end_date)

        self.assertEqual(
            week_data[1],
            [{'week_num': 52, 'year': 2019}, {'week_num': 1, 'year': 2020},
             {'week_num': 2, 'year': 2020}, {'week_num': 3, 'year': 2020}],
            'Calculates weeks 52, 2019 to 3, 2020'
        )

    def test_compute_weeks_start_week_end_week_changed(self):
        """
        Tests if compute_weeks returns an empty array if end_date is before the start_date

        """
        start_date = datetime(2020, 1, 17, 7, 30, 25)
        end_date = datetime(2019, 12, 27, 0, 0, 0)

        week_data = self.env['resource.model'].compute_weeks(start_date, end_date)

        self.assertEqual(week_data[1], [], 'No weeks because start and end date are interchanged')

    def test_compute_weeks_normal_result_one_week(self):
        """
        Tests if the returned array from the compute_weeks method contains the correct weeks
        (a single week)

        """
        start_date = datetime(2020, 11, 10, 20, 45, 25)
        end_date = datetime(2020, 11, 14, 4, 30, 25)

        week_data = self.env['resource.model'].compute_weeks(start_date, end_date)

        self.assertEqual(week_data[1], [{'week_num': 46, 'year': 2020}], 'Result is only one week (46)')

    # -------------------------------------------------------------------------------------------------------------------- #

    def test_add_weeks_object_normal(self):
        """
        Tests if add_weeks_objects preserves the week number and year
        (part 1)

        """
        week = self.env['resource.model'].add_weeks_object({'week_num': 52, 'year': 2020})
        self.assertEqual(week.week_num, 52, 'Week number is 52')
        self.assertEqual(week.year, 2020, 'Year is 2020')

    def test_add_weeks_object_normal_2(self):
        """
        Tests if add_weeks_objects preserves the week number and year
        (part 2)

        """
        week = self.env['resource.model'].add_weeks_object({'week_num': 52, 'year': 2050})
        self.assertNotEqual(week.week_num, 1, 'Week number is not 1')
        self.assertNotEqual(week.year, 2020, 'Year is not 2020')

    def test_add_weeks_object_old_year(self):
        """
        Tests if a week far in the past can be saved

        """
        week = self.env['resource.model'].add_weeks_object({'week_num': 50, 'year': 1901})
        self.assertEqual(week.week_num, 50, 'Week number is 50')
        self.assertEqual(week.year, 1901, 'Year is 1901')
        self.assertEqual(week.week_string, "1901, W50", "Invalid week_string")

    def test_add_weeks_object_future_year(self):
        """
        Tests if a week far in the future can be saved

        """
        week = self.env['resource.model'].add_weeks_object({'week_num': 1, 'year': 3000})
        self.assertEqual(week.week_num, 1, 'Week number is 1')
        self.assertEqual(week.year, 3000, 'Year is 3000')
        self.assertEqual(week.week_string, "3000, W01", "Invalid week_string")

    # -------------------------------------------------------------------------------------------------------------------- #

    def test_create_resource_normal(self):
        """
        Tests if create stores the values (project, employee, workload, start_date, end_dat) correctly
        (part 1, workload 50)

        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 50,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}
        resource = self.env['resource.model'].create(values)

        manual_start_date = datetime(2020, 4, 5, 13, 42, 7)
        manual_end_date = datetime(2020, 4, 12, 13, 42, 7)

        self.assertEqual(resource.project.id, project.id, "project id doesn't match")
        self.assertEqual(resource.employee.id, employee.id, "employee id doesn't match")
        self.assertEqual(resource.base_workload, 50, "workload should be 50")
        self.assertEqual(resource.start_date, manual_start_date, "start_date should be '2020-04-05 13:42:07'")
        self.assertEqual(resource.end_date, manual_end_date, "end_date should be '2020-04-12 13:42:07'")

    def test_create_resource_normal_2(self):
        """
        Tests if create stores the values (project, employee, workload, start_date, end_dat) correctly
        (part 2, workload 90)

        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 90,
                  'start_date': '2020-04-13 13:59:40',
                  'end_date': '2020-05-22 13:59:40'}
        resource = self.env['resource.model'].create(values)

        manual_start_date = datetime(2020, 4, 13, 13, 59, 40)
        manual_end_date = datetime(2020, 5, 22, 13, 59, 40)

        self.assertEqual(resource.project.id, project.id, "project id doesn't match")
        self.assertEqual(resource.employee.id, employee.id, "employee id doesn't match")
        self.assertEqual(resource.base_workload, 90, "workload should be 90")
        self.assertEqual(resource.start_date, manual_start_date, "start_date should be '2020-04-13 13:59:40'")
        self.assertEqual(resource.end_date, manual_end_date, "end_date should be '2020-05-22 13:59:40'")

    def test_create_resource_normal_3(self):
        """
        Tests if create stores the values (project, employee, workload, start_date, end_dat) correctly
        (part 3, workload 100)

        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 100,
                  'start_date': '2020-04-19 14:12:04',
                  'end_date': '2020-05-03 14:12:04'}
        resource = self.env['resource.model'].create(values)

        manual_start_date = datetime(2020, 4, 19, 14, 12, 4)
        manual_end_date = datetime(2020, 5, 3, 14, 12, 4)

        self.assertEqual(resource.project.id, project.id, "project id doesn't match")
        self.assertEqual(resource.employee.id, employee.id, "employee id doesn't match")
        self.assertEqual(resource.base_workload, 100, "workload should be 100")
        self.assertEqual(resource.start_date, manual_start_date, "start_date should be '2020-04-19 14:12:04'")
        self.assertEqual(resource.end_date, manual_end_date, "end_date should be '2020-05-03 14:12:04'")

    def test_create_resource_normal_start_date_equals_end_date(self):
        """
        Tests if create stores the values (project, employee, workload, start_date, end_dat) correctly
        (part 4, start_date equals end_date)

        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 100,
                  'start_date': '2020-05-03 14:12:04',
                  'end_date': '2020-05-03 14:12:04'}
        resource = self.env['resource.model'].create(values)

        manual_start_date = datetime(2020, 5, 3, 14, 12, 4)
        manual_end_date = datetime(2020, 5, 3, 14, 12, 4)

        self.assertEqual(resource.project.id, project.id, "project id doesn't match")
        self.assertEqual(resource.employee.id, employee.id, "employee id doesn't match")
        self.assertEqual(resource.base_workload, 100, "workload should be 100")
        self.assertEqual(resource.start_date, manual_start_date, "start_date should be '2020-05-03 14:12:04'")
        self.assertEqual(resource.end_date, manual_end_date, "end_date should be '2020-05-03 14:12:04'")

    def test_create_resource_exception_start_after_end_date_1(self):
        """
        Tests if create raises an exception if the start_date is after the end_date
        (part 1, same year)

        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 100,
                  'start_date': '2020-05-03 14:12:04',
                  'end_date': '2020-04-19 14:12:04'}

        with self.assertRaises(exceptions.ValidationError)as error:
            self.env['resource.model'].create(values)

        self.assertEqual(error.exception.name,
                         "Start date must be before end date", "Should raise exception if start is after"
                                                               "end dates")

    def test_create_resource_exception_start_after_end_date_2(self):
        """
        Tests if create raises an exception if the start_date is after the end_date
        (part 2, different years)

        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 100,
                  'start_date': '2019-05-03 14:12:04',
                  'end_date': '2018-04-19 14:12:04'}

        with self.assertRaises(exceptions.ValidationError)as error:
            self.env['resource.model'].create(values)

        self.assertEqual(error.exception.name,
                         "Start date must be before end date", "Should raise exception if start is after"
                                                               "end dates")

    def test_create_resource_exception_no_start_date(self):
        """
                Tests if create raises an exception if the start_date is not filled out
        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 100,
                  'start_date': False,
                  'end_date': '2018-04-19 14:12:04'}

        with self.assertRaises(exceptions.ValidationError)as error:
            self.env['resource.model'].create(values)

        self.assertEqual(error.exception.name,
                         "Both dates must be filled out", "Should raise exception if start_date"
                                                          "is not filled out")

    def test_create_resource_exception_no_end_date(self):
        """
                Tests if create raises an exception if the end_date is not filled out
        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 100,
                  'start_date': '2018-04-19 14:12:04',
                  'end_date': False}

        with self.assertRaises(exceptions.ValidationError)as error:
            self.env['resource.model'].create(values)

        self.assertEqual(error.exception.name,
                         "Both dates must be filled out", "Should raise exception if end_date"
                                                          "is not filled out")

    def test_create_resource_exception_no_start_no_end_date(self):
        """
                Tests if create raises an exception if the end_date and the start_date are not filled out
        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 100,
                  'start_date': False,
                  'end_date': False}

        with self.assertRaises(exceptions.ValidationError)as error:
            self.env['resource.model'].create(values)

        self.assertEqual(error.exception.name,
                         "Both dates must be filled out", "Should raise exception if start and"
                                                          "end dates are not filled out")

    def test_create_resource_no_project(self):
        """
          Tests if create raises an exception if the employee is not given
          displays error message in console, error message is intended
        """
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': '',
                  'employee': employee.id,
                  'base_workload': 100,
                  'start_date': '2020-05-03 14:12:04',
                  'end_date': '2020-04-19 14:12:04'}

        with self.assertRaises(errors.NotNullViolation):
            self.env['resource.model'].create(values)

    def test_create_resource_no_employee(self):
        """
            Tests if create raises an exception if the employee is not given
             displays error message in console, error message is intended
        """
        project = self.env['project.project'].create({'name': 'p1'})
        values = {'project': project.id,
                  'employee': '',
                  'base_workload': 100,
                  'start_date': '2020-05-03 14:12:04',
                  'end_date': '2020-04-19 14:12:04'}

        with self.assertRaises(errors.NotNullViolation):
            self.env['resource.model'].create(values)

    # -------------------------------------------------------------------------------------------------------------------- #

    def test_verify_workload_warning_1(self):
        """
        Tests if an exception is raised if workload exceeds 100
        (part 1, 101)

        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 101,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}

        with self.assertRaises(exceptions.ValidationError) as e:
            self.env['resource.model'].create(values)

        self.assertEqual(e.exception.name,
                         "The given workload can't be larger than 100 %",
                         "Should raise exception for workload being to high")

    def test_verify_workload_warning_2(self):
        """
        Tests if an exception is raised if workload exceeds 100
        (part 2, 1000)

        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 1000,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}

        with self.assertRaises(exceptions.ValidationError) as e:
            self.env['resource.model'].create(values)

        self.assertEqual(e.exception.name,
                         "The given workload can't be larger than 100 %",
                         "Should raise exception for workload being to high")

    def test_verify_workload_warning_3(self):
        """
        Tests if an exception is raised if workload exceeds 100
        (part 3, 3243200)

        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 3243200,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}

        with self.assertRaises(exceptions.ValidationError) as e:
            self.env['resource.model'].create(values)

        self.assertEqual(e.exception.name,
                         "The given workload can't be larger than 100 %",
                         "Should raise exception for workload being to high")

    def test_verify_workload_warning_4(self):
        """
        Tests if an exception is raised if workload falls below 0

        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': -10,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}

        with self.assertRaises(exceptions.ValidationError) as e:
            self.env['resource.model'].create(values)

        self.assertEqual(e.exception.name,
                         "The given workload can't be smaller than 0 %",
                         "Should raise exception for workload being to low")

    def test_verify_no_workload_warning_1(self):
        """
        Tests if no exception is raised if workload is exactly 0

        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 0,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}

        resource = self.env['resource.model'].create(values)

        self.assertEqual(resource.verify_workload(), None, 'Warning is not shown (0%)')

    def test_verify_workload_no_warning_2(self):
        """
        Tests if no exception is raised if workload is exactly 100

        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 100,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}

        resource = self.env['resource.model'].create(values)

        self.assertEqual(resource.verify_workload(), None, 'Warning is not shown (100%)')

    def test_verify_workload_no_warning_3(self):
        """
        Tests if no exception is raised if workload is exactly 1

        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 1,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}
        resource = self.env['resource.model'].create(values)

        self.assertEqual(resource.verify_workload(), None, 'Warning is not shown (1%)')

    # -------------------------------------------------------------------------------------------------------------------- #

    def test_write_resource_project(self):
        """
        Tests if write stores the values (project, employee, workload, start_date, end_dat) correctly
        (part 1, overwrite project)

        """
        # Step 1: Create project
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 50,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}
        resource = self.env['resource.model'].create(values)

        # Step 2: Update project
        project2 = self.env['project.project'].create({'name': 'p2'})
        values = {'project': project2.id,
                  'employee': employee.id,
                  'base_workload': 50,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}

        # Step 2: Update project
        resource.write(values)

        # Step 3: Evaluate Values
        manual_start_date = datetime(2020, 4, 5, 13, 42, 7)
        manual_end_date = datetime(2020, 4, 12, 13, 42, 7)

        self.assertEqual(resource.project.id, project2.id, "project id doesn't match")
        self.assertEqual(resource.employee.id, employee.id, "employee id doesn't match")
        self.assertEqual(resource.base_workload, 50, "workload should be 50")
        self.assertEqual(resource.start_date, manual_start_date, "start_date should be '2020-04-05 13:42:07'")
        self.assertEqual(resource.end_date, manual_end_date, "end_date should be '2020-04-12 13:42:07'")

    def test_write_resource_employee(self):
        """
        Tests if write updates the values correctly
        (part 2, update employee)

        """
        # Step 1: Create project
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 50,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}
        resource = self.env['resource.model'].create(values)

        # Step 2: Update project
        employee2 = self.env['hr.employee'].create({'name': 'e2'})
        values = {'project': project.id,
                  'employee': employee2.id,
                  'base_workload': 50,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}
        resource.write(values)

        # Step 3: Evaluate values
        manual_start_date = datetime(2020, 4, 5, 13, 42, 7)
        manual_end_date = datetime(2020, 4, 12, 13, 42, 7)

        self.assertEqual(resource.project.id, project.id, "project id doesn't match")
        self.assertEqual(resource.employee.id, employee2.id, "employee id doesn't match")
        self.assertEqual(resource.base_workload, 50, "workload should be 50")
        self.assertEqual(resource.start_date, manual_start_date, "start_date should be '2020-04-05 13:42:07'")
        self.assertEqual(resource.end_date, manual_end_date, "end_date should be '2020-04-12 13:42:07'")

    def test_write_resource_workload(self):
        """
        Tests if write updates the values correctly
        (part 3, update workload)

        """
        # Step 1: Create project
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 50,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}
        resource = self.env['resource.model'].create(values)

        # Step 2: Update project
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 99,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}
        resource.write(values)

        # Step 3: Evaluate Values
        manual_start_date = datetime(2020, 4, 5, 13, 42, 7)
        manual_end_date = datetime(2020, 4, 12, 13, 42, 7)

        self.assertEqual(resource.project.id, project.id, "project id doesn't match")
        self.assertEqual(resource.employee.id, employee.id, "employee id doesn't match")
        self.assertEqual(resource.base_workload, 99, "workload should be 99")
        self.assertEqual(resource.start_date, manual_start_date, "start_date should be '2020-04-05 13:42:07'")
        self.assertEqual(resource.end_date, manual_end_date, "end_date should be '2020-04-12 13:42:07'")

    def test_write_resource_dates(self):
        """
        Tests if write updates the values correctly
        (part 4, update start_date and end_date)

        """
        # Step 1: Create project
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 50,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}
        resource = self.env['resource.model'].create(values)

        # Step 2: Update project
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 50,
                  'start_date': '2020-04-13 13:42:07',
                  'end_date': '2020-04-19 13:42:07'}
        resource.write(values)

        # Step 3: Evaluate Values
        manual_start_date = datetime(2020, 4, 13, 13, 42, 7)
        manual_end_date = datetime(2020, 4, 19, 13, 42, 7)

        self.assertEqual(resource.project.id, project.id, "project id doesn't match")
        self.assertEqual(resource.employee.id, employee.id, "employee id doesn't match")
        self.assertEqual(resource.base_workload, 50, "workload should be 50")
        self.assertEqual(resource.start_date, manual_start_date, "start_date should be '2020-04-13 13:42:07'")
        self.assertEqual(resource.end_date, manual_end_date, "end_date should be '2020-04-19 13:42:07'")

    def test_write_resource_all(self):
        """
        Tests if write updates the values correctly
        (part 5, overwrite all values)

        """
        # Step 1: Create Resource
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 50,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}
        resource = self.env['resource.model'].create(values)

        # Step 2: Update Resource
        project2 = self.env['project.project'].create({'name': 'p2'})
        employee2 = self.env['hr.employee'].create({'name': 'e2'})
        values = {'project': project2.id,
                  'employee': employee2.id,
                  'base_workload': 99,
                  'start_date': '2020-04-13 13:42:07',
                  'end_date': '2020-04-19 13:42:07'}
        resource.write(values)

        # Step 3: Evaluate values
        manual_start_date = datetime(2020, 4, 13, 13, 42, 7)
        manual_end_date = datetime(2020, 4, 19, 13, 42, 7)

        self.assertEqual(resource.project.id, project2.id, "project id doesn't match")
        self.assertEqual(resource.employee.id, employee2.id, "employee id doesn't match")
        self.assertEqual(resource.base_workload, 99, "workload should be 99")
        self.assertEqual(resource.start_date, manual_start_date, "start_date should be '2020-04-13 13:42:07'")
        self.assertEqual(resource.end_date, manual_end_date, "end_date should be '2020-04-19 13:42:07'")

    def test_write_resource_start_date_equals_end_date(self):
        """
        Tests if write updates the values correctly
        (part 6, start_date equals end_date)

        """

        # Step 1: Create project
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 50,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}
        resource = self.env['resource.model'].create(values)

        # Step 2: Update values
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 50,
                  'start_date': '2020-05-03 14:12:04',
                  'end_date': '2020-05-03 14:12:04'}
        resource.write(values)

        # Step 3: Evaluate values
        manual_start_date = datetime(2020, 5, 3, 14, 12, 4)
        manual_end_date = datetime(2020, 5, 3, 14, 12, 4)

        self.assertEqual(resource.project.id, project.id, "project id doesn't match")
        self.assertEqual(resource.employee.id, employee.id, "employee id doesn't match")
        self.assertEqual(resource.base_workload, 50, "workload should be 50")
        self.assertEqual(resource.start_date, manual_start_date, "start_date should be '2020-05-03 14:12:04'")
        self.assertEqual(resource.end_date, manual_end_date, "end_date should be '2020-05-03 14:12:04'")

    def test_write_resource_start_after_end_date(self):
        """
        Tests if write raises an exception if the start_date is after the end_date
        (difference is only 1s)

        """

        # Step 1: Create project
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 50,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}
        resource = self.env['resource.model'].create(values)

        # Step 2: Update values
        # Expect ValidationError
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 50,
                  'start_date': '2020-05-03 14:12:04',
                  'end_date': '2020-05-03 14:12:03'}
        with self.assertRaises(exceptions.ValidationError):
            resource.write(values)

    # -------------------------------------------------------------------------------------------------------------------- #

    def test_create_single_week(self):
        """
        Tests whether the correct WeeklyResource models are created by create
        (part 1, resource during 1 week)

        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 50,
                  'start_date': '2020-04-06 13:42:07',
                  'end_date': '2020-04-10 13:42:07'}
        resource = self.env['resource.model'].create(values)

        weekly_model = self.env['weekly_resource.model']
        for model in weekly_model:
            if model.resource_id == resource.id:
                self.assertEqual(model.year, 2020, "Wrong year")
                self.assertEqual(model.week_num, 16, "Wrong week_num")
                self.assertEqual(model.week_string, "2020, W16", "Wrong week_string")
                self.assertEqual(model.weekly_workload, 50, 'Workload should be 50')

    def test_create_multiple_weeks(self):
        """
        Tests whether the correct WeeklyResource models are created by create
        (part 2, resource during 3 weeks)

        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 50,
                  'start_date': '2020-04-06 13:42:07',
                  'end_date': '2020-04-24 13:42:07'}
        resource = self.env['resource.model'].create(values)

        weekly_model = self.env['weekly_resource.model']
        for model in weekly_model:
            week = 16
            if model.resource_id == resource.id:
                self.assertEqual(model.year, 2020, "Wrong year")
                self.assertEqual(model.week_num, week, "Wrong week_num")
                self.assertEqual(model.week_string, "2020, W16", "Wrong week_string")
                self.assertEqual(model.weekly_workload, 50, "Workload should be 50")
                week = week + 1

    def test_write_single_to_multiple_weeks(self):
        """
        Tests whether the WeeklyResource models are updated correctly by write
        (part 1, update timespan from 1 week to 2 weeks)

        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 50,
                  'start_date': '2020-04-06 13:42:07',
                  'end_date': '2020-04-10 13:42:07'}
        resource = self.env['resource.model'].create(values)

        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 50,
                  'start_date': '2020-04-06 13:42:07',
                  'end_date': '2020-04-17 13:42:07'}
        resource.write(values)

        weekly_model = self.env['weekly_resource.model']
        for model in weekly_model:
            week = 16
            if model.resource_id == resource.id:
                self.assertEqual(model.year, 2020, "Wrong year")
                self.assertEqual(model.week_num, week, "Wrong week_num")
                self.assertEqual(model.weekly_workload, 50, "Workload should be 50")
                week = week + 1

    def test_write_multiple_to_single_week(self):
        """
        Tests whether the correct WeeklyResource models are created by write
        (part 2, update timespan from 4 weeks to 1 week)

        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 50,
                  'start_date': '2020-04-06 13:42:07',
                  'end_date': '2020-05-01 13:42:07'}
        resource = self.env['resource.model'].create(values)

        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 50,
                  'start_date': '2020-04-06 13:42:07',
                  'end_date': '2020-04-10 13:42:07'}
        resource.write(values)

        weekly_model = self.env['weekly_resource.model']
        for model in weekly_model:
            week = 16
            if model.resource_id == resource.id:
                self.assertEqual(model.year, 2020, "Wrong year")
                self.assertEqual(model.week_num, week, "Wrong week_num")
                self.assertNotEqual(model.week_num, 17, "Old WeeklyResource still exists")
                self.assertNotEqual(model.week_num, 18, "Old WeeklyResource still exists")
                self.assertNotEqual(model.week_num, 19, "Old WeeklyResource still exists")

    def test_write_delay_resource(self):
        """
        Tests whether the WeeklyResource models are updated correctly by write
        (part 3, delay resource)

        """

        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 50,
                  'start_date': '2020-04-06 13:42:07',
                  'end_date': '2020-04-10 13:42:07'}
        resource = self.env['resource.model'].create(values)

        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 50,
                  'start_date': '2020-04-20 13:42:07',
                  'end_date': '2020-04-24 13:42:07'}
        resource.write(values)

        weekly_model = self.env['weekly_resource.model']
        for model in weekly_model:
            if model.resource_id == resource.id:
                self.assertEqual(model.year, 2020, "Wrong year")
                self.assertEqual(model.week_num, 18, "Wrong week_num")
                self.assertNotEqual(model.week_num, 16, "Old WeeklyResource still exists")

    # -------------------------------------------------------------------------------------------------------------------- #

    def test_plus_one_week_normal(self):
        """
        Tests plus one week method whether it adds one week to the end date
        (part 1 same year)

         """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 1,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}
        resource = self.env['resource.model'].create(values)

        resource.plus_one_week()

        current_end_date = datetime.strptime('2020-04-12 13:42:07', '%Y-%m-%d %H:%M:%S') + timedelta(days=7)
        manual_start_date = datetime(2020, 4, 5, 13, 42, 7)

        self.assertEqual(current_end_date, resource.end_date, 'The resource was extended by 1 weeks')
        self.assertEqual(resource.start_date, manual_start_date, 'Start date got not changed')

    def test_plus_one_week_normal_push_button_twice(self):
        """
            Tests plus one week method whether it adds one week to the end date
            "button" pressed twice (method called twice)
             (part 1 same year)

        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 1,
                  'start_date': '2020-04-12 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}
        resource = self.env['resource.model'].create(values)

        resource.plus_one_week()
        resource.plus_one_week()

        current_end_date = datetime.strptime('2020-04-12 13:42:07', '%Y-%m-%d %H:%M:%S') + timedelta(days=14)
        manual_start_date = datetime(2020, 4, 12, 13, 42, 7)

        self.assertEqual(current_end_date, resource.end_date, 'The resource was extended by 2 weeks')
        self.assertEqual(resource.start_date, manual_start_date, 'Start date got not changed')

    def test_plus_one_week_normal_over_year_bound(self):
        """
        Tests plus one week method whether it adds one week to the end date
         (part 2 different year)

         """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 1,
                  'start_date': '2020-12-23 13:42:07',
                  'end_date': '2020-12-30 13:42:07'}
        resource = self.env['resource.model'].create(values)

        resource.plus_one_week()

        current_end_date = datetime.strptime('2020-12-30 13:42:07', '%Y-%m-%d %H:%M:%S') + timedelta(days=7)
        manual_start_date = datetime(2020, 12, 23, 13, 42, 7)

        self.assertEqual(current_end_date, resource.end_date,
                         'The resource was extended by 1 weeks over the year bound')
        self.assertEqual(resource.start_date, manual_start_date, 'Start date got not changed')

    def test_plus_minus_week_mix_normal(self):
        """
        Tests plus/minus one week method whether it subtracts and adds one week to/from the end date
        (part 1 same year)

         """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 1,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-06 13:42:07'}
        resource = self.env['resource.model'].create(values)

        resource.plus_one_week()
        resource.plus_one_week()
        resource.minus_one_week()
        resource.plus_one_week()
        resource.minus_one_week()
        resource.minus_one_week()

        current_end_date = datetime.strptime('2020-04-06 13:42:07', '%Y-%m-%d %H:%M:%S')
        manual_start_date = datetime(2020, 4, 5, 13, 42, 7)

        self.assertEqual(current_end_date, resource.end_date, 'The end date stayed the same')
        self.assertEqual(resource.start_date, manual_start_date, 'Start date got not changed')

    def test_plus_minus_one_week_mix_normal_over_year_bound(self):
        """
        Tests plus/minus one week method whether it adds and subtracts one week to/from the end date
         (part 2 different year)

         """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 1,
                  'start_date': '2020-12-23 13:42:07',
                  'end_date': '2020-12-30 13:42:07'}
        resource = self.env['resource.model'].create(values)

        resource.minus_one_week()
        resource.plus_one_week()
        resource.plus_one_week()
        resource.minus_one_week()
        resource.plus_one_week()
        resource.plus_one_week()
        resource.plus_one_week()

        current_end_date = datetime.strptime('2020-12-30 13:42:07', '%Y-%m-%d %H:%M:%S') + timedelta(days=21)
        manual_start_date = datetime(2020, 12, 23, 13, 42, 7)

        self.assertEqual(current_end_date, resource.end_date,
                         'The resource was extended by 1 weeks over the year bound')
        self.assertEqual(resource.start_date, manual_start_date, 'Start date got not changed')

    # -------------------------------------------------------------------------------------------------------------------- #

    def test_minus_one_week_normal(self):
        """
         Tests minus one week method whether it subtracts one week from the end date

        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 1,
                  'start_date': '2020-03-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}
        resource = self.env['resource.model'].create(values)

        resource.minus_one_week()

        current_end_date = datetime.strptime('2020-04-05 13:42:07', '%Y-%m-%d %H:%M:%S')
        manual_start_date = datetime(2020, 3, 5, 13, 42, 7)

        self.assertEqual(current_end_date, resource.end_date, 'The resource was reduced by 1 weeks')
        self.assertEqual(resource.start_date, manual_start_date, 'Start date got not changed')

    def test_minus_one_normal_button_pushed_three_times(self):
        """
            Tests minus one week method whether it subtracts one week from the end date
            "button" pushed 3 times (method called 3 times)

        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 1,
                  'start_date': '2020-03-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}
        resource = self.env['resource.model'].create(values)

        resource.minus_one_week()
        resource.minus_one_week()
        resource.minus_one_week()

        current_end_date = datetime.strptime('2020-04-12 13:42:07', '%Y-%m-%d %H:%M:%S') - timedelta(days=21)
        manual_start_date = datetime(2020, 3, 5, 13, 42, 7)

        self.assertEqual(current_end_date, resource.end_date, 'The resource was reduced by 3 weeks')
        self.assertEqual(resource.start_date, manual_start_date, 'Start date got not changed')

    def test_minus_one_normal_over_year_bound(self):
        """
            Tests minus one week method whether it subtracts one week from the end date
            (part 2 different years)

        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 1,
                  'start_date': '2020-12-05 13:42:07',
                  'end_date': '2021-01-12 13:42:07'}
        resource = self.env['resource.model'].create(values)

        resource.minus_one_week()
        resource.minus_one_week()

        current_end_date = datetime.strptime('2021-01-12 13:42:07', '%Y-%m-%d %H:%M:%S') - timedelta(days=14)
        manual_start_date = datetime(2020, 12, 5, 13, 42, 7)

        self.assertEqual(current_end_date, resource.end_date,
                         'The resource was reduced by 2 weeks over the year bounds')
        self.assertEqual(resource.start_date, manual_start_date, 'Start date got not changed')

    def test_minus_week_exception(self):
        """
        Tests minus one week method whether it subtracts one week from the end date
        :raises exception that the start date mustn't be after the end date

         """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 1,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-06 13:42:07'}
        resource = self.env['resource.model'].create(values)

        with self.assertRaises(exceptions.ValidationError)as error:
            resource.minus_one_week()

        self.assertEqual(error.exception.name,
                         "Start date must be before end date", "Should raise exception if start is after"
                                                               "end dates")


# -------------------------------------------------------------------------------------------------------------------- #


class TestWorkload(common.SavepointCase):
    """
    Class to test the weekly_workload validation
    """
    project = None
    employee = None

    @classmethod
    def setUpClass(cls):
        super(TestWorkload, cls).setUpClass()
        cls.project = cls.env['project.project'].create({'name': 'p1'})
        cls.employee = cls.env['hr.employee'].create({'name': 'e1'})

    def test_create_resource_weekly_workload_too_high_1(self):
        """
        Tests if creating two resources in the same week with a total workload of 110
        raises an exception.ValidationError for the workload in that week.

        """
        values = {'project': TestWorkload.project.id,
                  'employee': TestWorkload.employee.id,
                  'base_workload': 50,
                  'start_date': '2020-04-06 13:42:07',
                  'end_date': '2020-04-10 13:42:07'}
        self.env['resource.model'].create(values)

        values = {'project': TestWorkload.project.id,
                  'employee': TestWorkload.employee.id,
                  'base_workload': 60,
                  'start_date': '2020-04-06 13:42:07',
                  'end_date': '2020-04-10 13:42:07'}

        with self.assertRaises(exceptions.ValidationError)as error:
            self.env['resource.model'].create(values)

        self.assertEqual(error.exception.name,
                         "The workload in week 2020, W15 is too high", "Should raise exception for Workload too high")

    def test_create_resource_weekly_workload_too_high_2(self):
        """
        Tests if creating three resources in the same week with a total workload of 120
        raises an exception.ValidationError for the workload in that week.

        """
        values = {'project': TestWorkload.project.id,
                  'employee': TestWorkload.employee.id,
                  'base_workload': 40,
                  'start_date': '2020-04-13 13:42:07',
                  'end_date': '2020-04-22 13:42:07'}
        self.env['resource.model'].create(values)

        values = {'project': TestWorkload.project.id,
                  'employee': TestWorkload.employee.id,
                  'base_workload': 60,
                  'start_date': '2020-04-21 13:42:07',
                  'end_date': '2020-04-30 13:42:07'}
        self.env['resource.model'].create(values)

        values = {'project': TestWorkload.project.id,
                  'employee': TestWorkload.employee.id,
                  'base_workload': 20,
                  'start_date': '2020-04-02 13:42:07',
                  'end_date': '2020-04-24 13:42:07'}

        with self.assertRaises(exceptions.ValidationError)as error:
            self.env['resource.model'].create(values)

        self.assertEqual(error.exception.name,
                         "The workload in week 2020, W17 is too high", "Should raise exception for Workload too high")

    def test_create_resource_weekly_workload_too_high_3(self):
        """
        Tests if creating two resources in the same week with a total workload of 110
        raises an exception.ValidationError for the workload in that week.

        """
        values = {'project': TestWorkload.project.id,
                  'employee': TestWorkload.employee.id,
                  'base_workload': 40,
                  'start_date': '2020-05-05 13:42:07',
                  'end_date': '2020-05-08 13:42:07'}
        self.env['resource.model'].create(values)

        values = {'project': TestWorkload.project.id,
                  'employee': TestWorkload.employee.id,
                  'base_workload': 60,
                  'start_date': '2020-05-18 13:42:07',
                  'end_date': '2020-05-29 13:42:07'}
        self.env['resource.model'].create(values)

        values = {'project': TestWorkload.project.id,
                  'employee': TestWorkload.employee.id,
                  'base_workload': 50,
                  'start_date': '2020-05-04 13:42:07',
                  'end_date': '2020-05-22 13:42:07'}

        with self.assertRaises(exceptions.ValidationError)as error:
            self.env['resource.model'].create(values)

        self.assertEqual(error.exception.name,
                         "The workload in week 2020, W21 is too high", "Should raise exception for Workload too high")


# -------------------------------------------------------------------------------------------------------------------- #


class TestAddDelete(common.SavepointCase):
    """
    Class to test the add_missing_weekly_resources and
    delete_spare_weekly_resources methods in the Resource class.
    """
    resource = None
    start_date = None
    end_date = None

    @classmethod
    def setUpClass(cls):
        """
        Set up the test class by creating a resource with one
        weekly_resource in week 16, year 2020.

        """
        super(TestAddDelete, cls).setUpClass()
        project = cls.env['project.project'].create({'name': 'p1'})
        employee = cls.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 50,
                  'start_date': '2020-04-13 13:42:07',
                  'end_date': '2020-04-17 13:42:07'}
        cls.resource = cls.env['resource.model'].create(values)

        cls.start_date = datetime(2020, 4, 5, 13, 42, 7)
        cls.end_date = datetime(2020, 4, 12, 13, 42, 7)

        for week_num in range(16, 20):
            exists = cls.env['week.model'].search([['week_num', '=', week_num],
                                                   ['year', '=', 2020]])

            if not exists:
                cls.env['week.model'].create({'week_num': week_num, 'year': 2020})

    def test_setup(self):
        """
        Test if the resource created in setUpClass is correct.

        """
        weekly_resources = self.resource.weekly_resources
        self.assertEqual(len(weekly_resources), 1, 'resource should contain 1 weekly_resources')

        self.assertEqual(weekly_resources[0].week_id.week_num, 16, 'week_num should be 16')
        self.assertEqual(weekly_resources[0].week_id.year, 2020, 'year should be 2020')
        self.assertEqual(weekly_resources[0].weekly_workload, 50, 'weekly_workload should be 50')

    def test_add_weeks_1(self):
        """
        Test if adding one week adds one weekly_resource to the resource.

        """
        project_week_data = [{'week_num': 17, 'year': 2020}]
        TestAddDelete.resource.add_missing_weekly_resources(project_week_data)

        weekly_resources = TestAddDelete.resource.weekly_resources
        self.assertEqual(len(weekly_resources), 2, 'resource should contain 2 weekly_resources')

        week_nums = []
        years = []
        weekly_workloads = []
        for weekly_resource in weekly_resources:
            week_nums.append(weekly_resource.week_id.week_num)
            years.append(weekly_resource.week_id.year)
            weekly_workloads.append(weekly_resource.weekly_workload)

        self.assertEqual(len(week_nums), 2, 'should contain 2 weeks')
        self.assertEqual(len(years), 2, 'should contain 2 years')

        self.assertNotIn(15, week_nums, 'week_num 15 should not be in week_nums')
        self.assertIn(16, week_nums, 'week_num 16 should be in week_nums')
        self.assertIn(17, week_nums, 'week_num 17 should be in week_nums')
        self.assertNotIn(18, week_nums, 'week_num 18 should not be in week_nums')
        self.assertIn(2020, years, 'year 2020 should be in years')
        self.assertNotIn(2021, years, 'year 2021 should not be in years')

        week1 = [i for i in weekly_resources if (i.week_id.week_num == 16 and
                                                 i.week_id.year == 2020)]
        self.assertIsNotNone(week1, 'week1 should not be empty')
        self.assertEqual(len(week1), 1, 'week1 should contain 1 weekly_resource')
        self.assertEqual(week1[0].weekly_workload, 50, 'weekly_workload of week1 should be 50')

        week2 = [i for i in weekly_resources if (i.week_id.week_num == 17 and
                                                 i.week_id.year == 2020)]
        self.assertIsNotNone(week2, 'week2 should not be empty')
        self.assertEqual(len(week2), 1, 'week2 should contain 1 weekly_resource')
        self.assertEqual(week2[0].weekly_workload, 50, 'weekly_workload of week2 should be 50')

        self.assertNotEqual(week1, week2, 'week1 and week2 should not be the same')

    def test_add_weeks_2(self):
        """
        Test if adding a week for which already a weekly_workload exists doesn't
        change the existing weekly_resources workload.

        """
        TestAddDelete.resource.weekly_resources[0].weekly_workload = 20
        self.assertEqual(TestAddDelete.resource.weekly_resources[0].weekly_workload, 20)
        project_week_data = [{'week_num': 16, 'year': 2020},
                             {'week_num': 17, 'year': 2020}]
        TestAddDelete.resource.add_missing_weekly_resources(project_week_data)

        weekly_resources = TestAddDelete.resource.weekly_resources
        self.assertEqual(len(weekly_resources), 2, 'resource should contain 2 weekly_resources')

        week_nums = []
        years = []
        weekly_workloads = []
        for weekly_resource in weekly_resources:
            week_nums.append(weekly_resource.week_id.week_num)
            years.append(weekly_resource.week_id.year)
            weekly_workloads.append(weekly_resource.weekly_workload)

        self.assertEqual(len(week_nums), 2, 'should contain 2 weeks')
        self.assertEqual(len(years), 2, 'should contain 2 years')

        self.assertNotIn(15, week_nums, 'week_num 15 should not be in week_nums')
        self.assertIn(16, week_nums, 'week_num 16 should be in week_nums')
        self.assertIn(17, week_nums, 'week_num 17 should be in week_nums')
        self.assertNotIn(18, week_nums, 'week_num 18 should not be in week_nums')
        self.assertIn(2020, years, 'year 2020 should be in years')
        self.assertNotIn(2021, years, 'year 2021 should not be in years')

        week1 = [i for i in weekly_resources if (i.week_id.week_num == 16 and
                                                 i.week_id.year == 2020)]
        self.assertIsNotNone(week1, 'week1 should not be empty')
        self.assertEqual(len(week1), 1, 'week1 should contain 1 weekly_resource')
        self.assertEqual(week1[0].weekly_workload, 20, 'weekly_workload of week1 should be 20')

        week2 = [i for i in weekly_resources if (i.week_id.week_num == 17 and
                                                 i.week_id.year == 2020)]
        self.assertIsNotNone(week2, 'week2 should not be empty')
        self.assertEqual(len(week2), 1, 'week2 should contain 1 weekly_resource')
        self.assertEqual(week2[0].weekly_workload, 50, 'weekly_workload of week2 should be 50')

        self.assertNotEqual(week1, week2, 'week1 and week2 should not be the same')

    def test_add_delete_week_1(self):
        """
        Test if calling delete_spare_weekly_resources with empty project_week_data
        array deletes all weekly_resources of the resource.

        """
        project_week_data = [{'week_num': 17, 'year': 2020}]

        TestAddDelete.resource.add_missing_weekly_resources(project_week_data)
        TestAddDelete.resource.delete_spare_weekly_resources([])

        weekly_resources = TestAddDelete.resource.weekly_resources
        self.assertEqual(len(weekly_resources), 0, 'resource should contain 0 weekly_resources')

    def test_add_delete_week_2(self):
        """
        Test if adding and deleting weekly_resources to / from resource results
        in the correct weekly_resources existing.

        """
        project_week_data_add = [{'week_num': 17, 'year': 2020},
                                 {'week_num': 18, 'year': 2020},
                                 {'week_num': 19, 'year': 2020}]
        project_week_data_delete = [{'week_num': 17, 'year': 2020},
                                    {'week_num': 18, 'year': 2020}]

        TestAddDelete.resource.add_missing_weekly_resources(project_week_data_add)
        TestAddDelete.resource.delete_spare_weekly_resources(project_week_data_delete)

        weekly_resources = TestAddDelete.resource.weekly_resources
        self.assertEqual(len(weekly_resources), 2, 'resource should contain 2 weekly_resources')

        week_nums = []
        years = []
        weekly_workloads = []
        for weekly_resource in weekly_resources:
            week_nums.append(weekly_resource.week_id.week_num)
            years.append(weekly_resource.week_id.year)
            weekly_workloads.append(weekly_resource.weekly_workload)

        self.assertEqual(len(week_nums), 2, 'should contain 2 weeks')
        self.assertEqual(len(years), 2, 'should contain 2 years')

        self.assertNotIn(16, week_nums, 'week_num 15 should not be in week_nums')
        self.assertIn(17, week_nums, 'week_num 16 should be in week_nums')
        self.assertIn(18, week_nums, 'week_num 17 should be in week_nums')
        self.assertNotIn(19, week_nums, 'week_num 18 should not be in week_nums')
        self.assertIn(2020, years, 'year 2020 should be in years')
        self.assertNotIn(2021, years, 'year 2021 should not be in years')

        week1 = [i for i in weekly_resources if (i.week_id.week_num == 17 and
                                                 i.week_id.year == 2020)]
        self.assertIsNotNone(week1, 'week1 should not be empty')
        self.assertEqual(len(week1), 1, 'week1 should contain 1 weekly_resource')
        self.assertEqual(week1[0].weekly_workload, 50, 'weekly_workload of week1 should be 50')

        week2 = [i for i in weekly_resources if (i.week_id.week_num == 18 and
                                                 i.week_id.year == 2020)]
        self.assertIsNotNone(week2, 'week2 should not be empty')
        self.assertEqual(len(week2), 1, 'week2 should contain 1 weekly_resource')
        self.assertEqual(week2[0].weekly_workload, 50, 'weekly_workload of week2 should be 50')

        self.assertNotEqual(week1, week2, 'week1 and week2 should not be the same')

    def test_delete_week_1(self):
        """
        Test if calling delete_spare_weekly_resources with existing weekly_resource and additional
        non existing weekly_resource doesn't create or delete any weekly_resources.

        """
        project_week_data = [{'week_num': 16, 'year': 2020},
                             {'week_num': 17, 'year': 2020}]
        TestAddDelete.resource.delete_spare_weekly_resources(project_week_data)

        weekly_resources = TestAddDelete.resource.weekly_resources
        self.assertEqual(len(weekly_resources), 1, 'resource should contain 1 weekly_resources')

        self.assertEqual(weekly_resources[0].week_id.week_num, 16, 'week_num should be 16')
        self.assertEqual(weekly_resources[0].week_id.year, 2020, 'year should be 2020')
        self.assertEqual(weekly_resources[0].weekly_workload, 50, 'weekly_workload should be 50')

    def test_delete_week_2(self):
        """
        Test if calling delete_spare_weekly_resources with existing weekly_resource
        doesn't change its weekly_workload.

        """
        TestAddDelete.resource.weekly_resources[0].weekly_workload = 70
        self.assertEqual(TestAddDelete.resource.weekly_resources[0].weekly_workload, 70)
        project_week_data = [{'week_num': 16, 'year': 2020},
                             {'week_num': 17, 'year': 2020}]
        TestAddDelete.resource.delete_spare_weekly_resources(project_week_data)

        weekly_resources = TestAddDelete.resource.weekly_resources
        self.assertEqual(len(weekly_resources), 1, 'resource should contain 1 weekly_resources')

        self.assertEqual(weekly_resources[0].week_id.week_num, 16, 'week_num should be 16')
        self.assertEqual(weekly_resources[0].week_id.year, 2020, 'year should be 2020')
        self.assertEqual(weekly_resources[0].weekly_workload, 70, 'weekly_workload should be 70')
