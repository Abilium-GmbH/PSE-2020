from datetime import datetime
from odoo import exceptions
from odoo.tests import common


# testing the behaviour of the resource model
class TestResource(common.TransactionCase):

    def test_get_weeks_normal(self):
        start_date = datetime(2020, 4, 5, 23, 55, 0)
        end_date = datetime(2020, 4, 14, 12, 42, 7)

        week_data = self.env['resource.model'].get_weeks(start_date, end_date)

        self.assertEqual(
            week_data[1],
            [{'week_num': 14, 'year': 2020}, {'week_num': 15, 'year': 2020}, {'week_num': 16, 'year': 2020}],
            'Should calculate project weeks 14 to 16'
        )

    def test_get_weeks_normal_over_year_bound(self):
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
        start_date = datetime(2020, 1, 17, 7, 30, 25)
        end_date = datetime(2019, 12, 27, 0, 0, 0)

        week_data = self.env['resource.model'].get_weeks(start_date, end_date)

        self.assertEqual(week_data[1], [], 'No weeks because start and end date are interchanged')

    def test_get_weeks_normal_result_one_week(self):
        start_date = datetime(2020, 11, 10, 20, 45, 25)
        end_date = datetime(2020, 11, 14, 4, 30, 25)

        week_data = self.env['resource.model'].get_weeks(start_date, end_date)

        self.assertEqual(week_data[1], [{'week_num': 46, 'year': 2020}], 'Result is only one week (46)')

# -------------------------------------------------------------------------------------------------------------------- #

    def test_add_weeks_object_normal(self):
        week = self.env['resource.model'].add_weeks_object({'week_num': 52, 'year': 2020})
        self.assertEqual(week.week_num, 52, 'Week number is 52')
        self.assertEqual(week.year, 2020, 'Year is 2020')

    def test_add_weeks_object_normal_2(self):
        week = self.env['resource.model'].add_weeks_object({'week_num': 52, 'year': 2050})
        self.assertNotEqual(week.week_num, 1, 'Week number is not 1')
        self.assertNotEqual(week.year, 2020, 'Year is not 2020')

    def test_add_weeks_object_old_year(self):
        week = self.env['resource.model'].add_weeks_object({'week_num': 50, 'year': 1900})
        self.assertEqual(week.week_num, 50, 'Week number is 50')
        self.assertEqual(week.year, 1900, 'Year is 1900')

    def test_add_weeks_object_future_year(self):
        week = self.env['resource.model'].add_weeks_object({'week_num': 1, 'year': 3000})
        self.assertEqual(week.week_num, 1, 'Week number is 1')
        self.assertEqual(week.year, 3000, 'Year is 3000')

# -------------------------------------------------------------------------------------------------------------------- #

    def test_create_resource_normal(self):
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
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'workload': 1,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}
        resource = self.env['resource.model'].create(values)

        self.assertEqual(resource.verify_workload(), None, 'Warning is not shown (1%)')
