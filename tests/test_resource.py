from datetime import datetime
from odoo import exceptions
from odoo.tests import common


# testing the behaviour of the resource model
class TestResource(common.TransactionCase):

    def test_get_week_data_normal(self):
        start_week = 1
        start_year = 2020
        end_week = 3
        end_year = 2020

        week_data = self.env['resource.model'].get_week_data(start_week, start_year, end_week, end_year)

        self.assertEqual(
            week_data,
            [{'week_num': 1, 'year': 2020}, {'week_num': 2, 'year': 2020}, {'week_num': 3, 'year': 2020}],
            'Calculates weeks 1 to 3'
        )

    def test_get_week_data_normal_over_year_bound(self):
        start_week = 52
        start_year = 2019
        end_week = 3
        end_year = 2020

        week_data = self.env['resource.model'].get_week_data(start_week, start_year, end_week, end_year)
        print(week_data)

        self.assertEqual(
            week_data,
            [{'week_num': 52, 'year': 2019}, {'week_num': 1, 'year': 2020}, {'week_num': 2, 'year': 2020}, {'week_num': 3, 'year': 2020}],
            'Calculates weeks 52, 2019 to 3, 2020'
        )

    def test_get_week_data_start_week_end_week_changed(self):
        start_week = 3
        start_year = 2020
        end_week = 1
        end_year = 2020

        week_data = self.env['resource.model'].get_week_data(start_week, start_year, end_week, end_year)

        self.assertEqual(week_data, [], 'No weeks because start and end date are interchanged')

    def test_get_week_data_normal_result_one_week(self):
        start_week = 46
        start_year = 2020
        end_week = 46
        end_year = 2020

        week_data = self.env['resource.model'].get_week_data(start_week, start_year, end_week, end_year)

        self.assertEqual(week_data, [{'week_num': 46, 'year': 2020}], 'Result is only one week (46)')

    ##TODO fix that week 0 gets ignored test should fail!! wrong assertion
    def test_get_week_data_normal_with_zero(self):
        start_week = 0
        start_year = 2020
        end_week = 2
        end_year = 2020
        self.assertEqual(self.env['resource.model'].get_week_data(start_week, start_year, end_week, end_year),
                         [{'week_num': 1, 'year': 2020}, {'week_num': 2, 'year': 2020}],
                         'Result is week 1 and 2, week 0 gets ignored as starting week')

    ##TODO fix that week 0 gets ignored test should fail!! wrong assertion
    def test_get_week_data_normal_with_zero_at_end(self):
        start_week = 50
        start_year = 2020
        end_week = 0
        end_year = 2020
        self.assertEqual(self.env['resource.model'].get_week_data(start_week, start_year, end_week, end_year),
                         [{'week_num': 50, 'year': 2020}, {'week_num': 51, 'year': 2020},
                          {'week_num': 52, 'year': 2020}],
                         'Result is week 50, 51 and 52, week 0 gets ignored as ending week')

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
        resource = self.env['resource.model'].create(values)

        self.assertEqual(
            resource.verify_workload(),
            {'warning': {'title': "Workload too high", 'message': "The given workload is too high for an employee"}, },
            'Warning that workload is too high(101%) is shown')

    def test_verify_workload_warning_2(self):
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'workload': 1000,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}
        resource = self.env['resource.model'].create(values)

        self.assertEqual(
            resource.verify_workload(),
            {'warning': {'title': "Workload too high", 'message': "The given workload is too high for an employee"}, },
            'Warning that workload is too high(1000%) is shown')

    def test_verify_workload_warning_3(self):
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'workload': 1000,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}
        resource = self.env['resource.model'].create(values)

        self.assertNotEqual(
            resource.verify_workload(),
            {'title': "Workload too high", 'message': "The given workload is too high for an employee"},
            'Warning should not be the same')

    def test_verify_workload_warning_4(self):
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'workload': -10,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}
        resource = self.env['resource.model'].create(values)

        self.assertEqual(
            resource.verify_workload(),
            {'warning': {'title': "Workload too low", 'message': "The given workload can't be 0 or less"}, },
            'Warning that workload is too low (-10%) is shown')

    def test_verify_workload_warning_5(self):
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'workload': 0,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}
        resource = self.env['resource.model'].create(values)

        self.assertEqual(
            resource.verify_workload(),
            {'warning': {'title': "Workload too low", 'message': "The given workload can't be 0 or less"}, },
            'Warning that workload is too low (0%) is shown')

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
