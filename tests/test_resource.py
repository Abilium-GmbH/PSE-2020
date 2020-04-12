from datetime import datetime
from odoo import exceptions
from odoo.tests import common


class TestResource(common.TransactionCase):
    """
    Class to test the Resource class
    """

    def test_get_weeks_normal(self):
        """
        Tests if the returned array from the get_weeks method contains the correct weeks
        (multiple weeks)

        :return:
        """
        start_date = datetime(2020, 4, 5, 23, 55, 0)
        end_date = datetime(2020, 4, 14, 12, 42, 7)

        week_data = self.env['resource.model'].get_weeks(start_date, end_date)

        self.assertEqual(
            week_data[1],
            [{'week_num': 14, 'year': 2020}, {'week_num': 15, 'year': 2020}, {'week_num': 16, 'year': 2020}],
            'Should calculate project weeks 14 to 16'
        )

    def test_get_weeks_normal_over_year_bound(self):
        """
        Tests if get_weeks works correctly for at a turn of the year

        :return:
        """
        start_date = datetime(2019, 12, 27, 0, 0, 0)
        end_date = datetime(2020, 1, 17, 7, 30, 25)

        week_data = self.env['resource.model'].get_weeks(start_date, end_date)

        self.assertEqual(
            week_data[1],
            [{'week_num': 52, 'year': 2019}, {'week_num': 1, 'year': 2020},
             {'week_num': 2, 'year': 2020}, {'week_num': 3, 'year': 2020}],
            'Calculates weeks 52, 2019 to 3, 2020'
        )

    def test_get_weeks_start_week_end_week_changed(self):
        """
        Tests if get_weeks returns an empty array if end_date is before the start_date

        :return:
        """
        start_date = datetime(2020, 1, 17, 7, 30, 25)
        end_date = datetime(2019, 12, 27, 0, 0, 0)

        week_data = self.env['resource.model'].get_weeks(start_date, end_date)

        self.assertEqual(week_data[1], [], 'No weeks because start and end date are interchanged')

    def test_get_weeks_normal_result_one_week(self):
        """
        Tests if the returned array from the get_weeks method contains the correct weeks
        (a single week)

        :return:
        """
        start_date = datetime(2020, 11, 10, 20, 45, 25)
        end_date = datetime(2020, 11, 14, 4, 30, 25)

        week_data = self.env['resource.model'].get_weeks(start_date, end_date)

        self.assertEqual(week_data[1], [{'week_num': 46, 'year': 2020}], 'Result is only one week (46)')

# -------------------------------------------------------------------------------------------------------------------- #

    def test_add_weeks_object_normal(self):
        """
        Tests if add_weeks_objects preserves the week number and year
        (part 1)

        :return:
        """
        week = self.env['resource.model'].add_weeks_object({'week_num': 52, 'year': 2020})
        self.assertEqual(week.week_num, 52, 'Week number is 52')
        self.assertEqual(week.year, 2020, 'Year is 2020')

    def test_add_weeks_object_normal_2(self):
        """
        Tests if add_weeks_objects preserves the week number and year
        (part 2)

        :return:
        """
        week = self.env['resource.model'].add_weeks_object({'week_num': 52, 'year': 2050})
        self.assertNotEqual(week.week_num, 1, 'Week number is not 1')
        self.assertNotEqual(week.year, 2020, 'Year is not 2020')

    def test_add_weeks_object_old_year(self):
        """
        Tests if a week far in the past can be saved

        :return:
        """
        week = self.env['resource.model'].add_weeks_object({'week_num': 50, 'year': 1900})
        self.assertEqual(week.week_num, 50, 'Week number is 50')
        self.assertEqual(week.year, 1900, 'Year is 1900')

    def test_add_weeks_object_future_year(self):
        """
        Tests if a week far in the future can be saved

        :return:
        """
        week = self.env['resource.model'].add_weeks_object({'week_num': 1, 'year': 3000})
        self.assertEqual(week.week_num, 1, 'Week number is 1')
        self.assertEqual(week.year, 3000, 'Year is 3000')

# -------------------------------------------------------------------------------------------------------------------- #

    def test_create_resource_normal(self):
        """
        Tests if create stores the values (project, employee, workload, start_date, end_dat) correctly
        (part 1, workload 50)

        :return:
        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'workload': 50,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}
        resource = self.env['resource.model'].create(values)

        manual_start_date = datetime(2020, 4, 5, 13, 42, 7)
        manual_end_date = datetime(2020, 4, 12, 13, 42, 7)

        self.assertEqual(resource.project.id, project.id, "project id doesn't match")
        self.assertEqual(resource.employee.id, employee.id, "employee id doesn't match")
        self.assertEqual(resource.workload, 50, "workload should be 50")
        self.assertEqual(resource.start_date, manual_start_date, "start_date should be '2020-04-05 13:42:07'")
        self.assertEqual(resource.end_date, manual_end_date, "end_date should be '2020-04-12 13:42:07'")

    def test_create_resource_normal_2(self):
        """
        Tests if create stores the values (project, employee, workload, start_date, end_dat) correctly
        (part 2, workload 90)

        :return:
        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'workload': 90,
                  'start_date': '2020-04-13 13:59:40',
                  'end_date': '2020-05-22 13:59:40'}
        resource = self.env['resource.model'].create(values)

        manual_start_date = datetime(2020, 4, 13, 13, 59, 40)
        manual_end_date = datetime(2020, 5, 22, 13, 59, 40)

        self.assertEqual(resource.project.id, project.id, "project id doesn't match")
        self.assertEqual(resource.employee.id, employee.id, "employee id doesn't match")
        self.assertEqual(resource.workload, 90, "workload should be 90")
        self.assertEqual(resource.start_date, manual_start_date, "start_date should be '2020-04-13 13:59:40'")
        self.assertEqual(resource.end_date, manual_end_date, "end_date should be '2020-05-22 13:59:40'")

    def test_create_resource_normal_3(self):
        """
        Tests if create stores the values (project, employee, workload, start_date, end_dat) correctly
        (part 3, workload 100)

        :return:
        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'workload': 100,
                  'start_date': '2020-04-19 14:12:04',
                  'end_date': '2020-05-03 14:12:04'}
        resource = self.env['resource.model'].create(values)

        manual_start_date = datetime(2020, 4, 19, 14, 12, 4)
        manual_end_date = datetime(2020, 5, 3, 14, 12, 4)

        self.assertEqual(resource.project.id, project.id, "project id doesn't match")
        self.assertEqual(resource.employee.id, employee.id, "employee id doesn't match")
        self.assertEqual(resource.workload, 100, "workload should be 100")
        self.assertEqual(resource.start_date, manual_start_date, "start_date should be '2020-04-19 14:12:04'")
        self.assertEqual(resource.end_date, manual_end_date, "end_date should be '2020-05-03 14:12:04'")

    def test_create_resource_normal_start_date_equals_end_date(self):
        """
        Tests if create stores the values (project, employee, workload, start_date, end_dat) correctly
        (part 4, start_date equals end_date)

        :return:
        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'workload': 100,
                  'start_date': '2020-05-03 14:12:04',
                  'end_date': '2020-05-03 14:12:04'}
        resource = self.env['resource.model'].create(values)

        manual_start_date = datetime(2020, 5, 3, 14, 12, 4)
        manual_end_date = datetime(2020, 5, 3, 14, 12, 4)

        self.assertEqual(resource.project.id, project.id, "project id doesn't match")
        self.assertEqual(resource.employee.id, employee.id, "employee id doesn't match")
        self.assertEqual(resource.workload, 100, "workload should be 100")
        self.assertEqual(resource.start_date, manual_start_date, "start_date should be '2020-05-03 14:12:04'")
        self.assertEqual(resource.end_date, manual_end_date, "end_date should be '2020-05-03 14:12:04'")

    def test_create_resource_exception_start_after_end_date_1(self):
        """
        Tests if create raises an exception if the start_date is after the end_date
        (part 1, same year)

        :return:
        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'workload': 100,
                  'start_date': '2020-05-03 14:12:04',
                  'end_date': '2020-04-19 14:12:04'}

        with self.assertRaises(exceptions.ValidationError):
            self.env['resource.model'].create(values)

    def test_create_resource_exception_start_after_end_date_2(self):
        """
        Tests if create raises an exception if the start_date is after the end_date
        (part 2, different years)

        :return:
        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'workload': 100,
                  'start_date': '2019-05-03 14:12:04',
                  'end_date': '2018-04-19 14:12:04'}

        with self.assertRaises(exceptions.ValidationError):
            self.env['resource.model'].create(values)

# -------------------------------------------------------------------------------------------------------------------- #

    def test_verify_workload_warning_1(self):
        """
        Tests if an exception is raised if workload exceeds 100
        (part 1, 101)

        :return:
        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'workload': 101,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}

        with self.assertRaises(exceptions.ValidationError) as e:
            self.env['resource.model'].create(values)

        self.assertEqual(e.exception.name,
                         "The given workload can't larger than 100",
                         "Should raise exception for workload being to high")

    def test_verify_workload_warning_2(self):
        """
        Tests if an exception is raised if workload exceeds 100
        (part 2, 1000)

        :return:
        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'workload': 1000,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}

        with self.assertRaises(exceptions.ValidationError) as e:
            self.env['resource.model'].create(values)

        self.assertEqual(e.exception.name,
                         "The given workload can't larger than 100",
                         "Should raise exception for workload being to high")

    def test_verify_workload_warning_3(self):
        """
        Tests if an exception is raised if workload exceeds 100
        (part 3, 3243200)

        :return:
        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'workload': 3243200,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}

        with self.assertRaises(exceptions.ValidationError) as e:
            self.env['resource.model'].create(values)

        self.assertEqual(e.exception.name,
                         "The given workload can't larger than 100",
                         "Should raise exception for workload being to high")

    def test_verify_workload_warning_4(self):
        """
        Tests if an exception is raised if workload falls below 0

        :return:
        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'workload': -10,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}

        with self.assertRaises(exceptions.ValidationError) as e:
            self.env['resource.model'].create(values)

        self.assertEqual(e.exception.name,
                         "The given workload can't be equal or smaller than 0",
                         "Should raise exception for workload being to low")

    def test_verify_workload_warning_5(self):
        """
        Tests if an exception is raised if workload is exactly 0

        :return:
        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'workload': 0,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}

        with self.assertRaises(exceptions.ValidationError) as e:
            self.env['resource.model'].create(values)

        self.assertEqual(e.exception.name,
                         "The given workload can't be equal or smaller than 0",
                         "Should raise exception for workload being to low")

    def test_verify_workload_no_warning_1(self):
        """
        Tests if no exception is raised if workload is exactly 100

        :return:
        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'workload': 100,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}

        resource = self.env['resource.model'].create(values)

        self.assertEqual(resource.verify_workload(), None, 'Warning is not shown (100%)')

    def test_verify_workload_no_warning_2(self):
        """
        Tests if no exception is raised if workload is exactly 1

        :return:
        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'workload': 1,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}
        resource = self.env['resource.model'].create(values)

        self.assertEqual(resource.verify_workload(), None, 'Warning is not shown (1%)')

# -------------------------------------------------------------------------------------------------------------------- #
    def test_write_resource_project(self):
        """
        Tests if write stores the values (project, employee, workload, start_date, end_dat) correctly
        (part 1, overwrite project)

        :return:
        """
        # Step 1: Create project
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'workload': 50,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}
        resource = self.env['resource.model'].create(values)
        project2 = self.env['project.project'].create({'name': 'p2'})
        values = {'project': project2.id,
                  'employee': employee.id,
                  'workload': 50,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}
        # Step 2: Update project
        resource.write(values)

        manual_start_date = datetime(2020, 4, 5, 13, 42, 7)
        manual_end_date = datetime(2020, 4, 12, 13, 42, 7)

        self.assertEqual(resource.project.id, project2.id, "project id doesn't match")
        self.assertEqual(resource.employee.id, employee.id, "employee id doesn't match")
        self.assertEqual(resource.workload, 50, "workload should be 50")
        self.assertEqual(resource.start_date, manual_start_date, "start_date should be '2020-04-05 13:42:07'")
        self.assertEqual(resource.end_date, manual_end_date, "end_date should be '2020-04-12 13:42:07'")



