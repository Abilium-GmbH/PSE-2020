from datetime import datetime
from odoo import exceptions
from odoo.tests import common


class TestIntegration1(common.SingleTransactionCase):
    """
    This test tests a basic sequence of steps performed by a user.
    """
    project_1 = None
    project_2 = None
    project_3 = None
    employee_1 = None
    resource_1 = None
    resource_2 = None
    resource_3 = None

    def test_01_create_resource_1(self):
        """
        Tests the creation of a resource.

        """
        TestIntegration1.project_1 = self.env['project.project'].create({'name': 'test_project_1'})
        TestIntegration1.employee_1 = self.env['hr.employee'].create({'name': 'test_employee_1'})
        values = {'project': TestIntegration1.project_1.id,
                  'employee': TestIntegration1.employee_1.id,
                  'base_workload': 70,
                  'start_date': '1990-06-13 12:00:00',
                  'end_date': '1990-12-04 12:00:00'}
        TestIntegration1.resource_1 = self.env['resource.model'].create(values)

        start_date = datetime(1990, 6, 13, 12, 0, 0)
        end_date = datetime(1990, 12, 4, 12, 0, 0)

        self.assertEqual(TestIntegration1.resource_1.project.id, TestIntegration1.project_1.id,
                         "project id doesn't match")
        self.assertEqual(TestIntegration1.resource_1.employee.id, TestIntegration1.employee_1.id,
                         "employee id doesn't match")
        self.assertEqual(TestIntegration1.resource_1.base_workload, 70, "base_workload should be 70")
        self.assertEqual(TestIntegration1.resource_1.start_date, start_date,
                         "start_date should be '1990-06-13 12:00:00'")
        self.assertEqual(TestIntegration1.resource_1.end_date, end_date, "end_date should be '1990-12-4 12:00:00'")

        for weekly_resource in TestIntegration1.resource_1.weekly_resources:
            self.assertEqual(weekly_resource.resource_id.id, TestIntegration1.resource_1.id,
                             "resource_id doesn't match")
            self.assertEqual(weekly_resource.weekly_workload, 70, "weekly_workload should be 70")

    def test_02_edit_base_workload_1(self):
        """
        Tests the editing of the base workload of a resource.

        """
        values = {
            'base_workload': 10
        }

        TestIntegration1.resource_1.write(values)

        start_date = datetime(1990, 6, 13, 12, 0, 0)
        end_date = datetime(1990, 12, 4, 12, 0, 0)

        self.assertEqual(TestIntegration1.resource_1.project.id, TestIntegration1.project_1.id,
                         "project id doesn't match")
        self.assertEqual(TestIntegration1.resource_1.employee.id, TestIntegration1.employee_1.id,
                         "employee id doesn't match")
        self.assertEqual(TestIntegration1.resource_1.base_workload, 10, "base_workload should be 10")
        self.assertEqual(TestIntegration1.resource_1.start_date, start_date,
                         "start_date should be '1990-06-13 12:00:00'")
        self.assertEqual(TestIntegration1.resource_1.end_date, end_date, "end_date should be '1990-12-4 12:00:00'")

        for weekly_resource in TestIntegration1.resource_1.weekly_resources:
            self.assertEqual(weekly_resource.resource_id.id, TestIntegration1.resource_1.id,
                             "resource_id doesn't match")
            self.assertEqual(weekly_resource.weekly_workload, 10, "weekly_workload should be 10")

    def test_03_edit_weekly_resource_1(self):
        """
        Tests the editing of the weekly workload of a weekly resource.

        """
        weekly_resource = TestIntegration1.resource_1.weekly_resources[10]
        weekly_resource.write({'weekly_workload': 50})

        self.assertEqual(TestIntegration1.resource_1.base_workload, 10, "base_workload should be 10")
        self.assertEqual(weekly_resource.weekly_workload, 50, "weekly_workload should be 50")

    def test_04_edit_base_workload_2(self):
        """
        Tests if editing the base workload of the resource doesn't
        affect the previously changed weekly workload of a weekly resource.

        """
        TestIntegration1.resource_1.write({'base_workload': 60})

        self.assertEqual(TestIntegration1.resource_1.project.id, TestIntegration1.project_1.id,
                         "project id doesn't match")
        self.assertEqual(TestIntegration1.resource_1.employee.id, TestIntegration1.employee_1.id,
                         "employee id doesn't match")
        self.assertEqual(TestIntegration1.resource_1.base_workload, 60, "base_workload should be 60")

        weekly_resources = TestIntegration1.resource_1.weekly_resources

        for i in range(0, len(weekly_resources)):
            self.assertEqual(weekly_resources[i].resource_id.id, TestIntegration1.resource_1.id,
                             "resource_id doesn't match")

            if i == 10:
                self.assertEqual(weekly_resources[i].weekly_workload, 50, "weekly_workload should be 50")
            else:
                self.assertEqual(weekly_resources[i].weekly_workload, 60, "weekly_workload should be 60")

    def test_05_create_resource_2(self):
        """
        Tests if creating a second resource raises a validation error when the
        base workload is too high and doesn't if not.

        """
        TestIntegration1.project_2 = self.env['project.project'].create({'name': 'test_project_2'})
        values = {'project': TestIntegration1.project_2.id,
                  'employee': TestIntegration1.employee_1.id,
                  'base_workload': 50,
                  'start_date': '1990-10-06 12:00:00',
                  'end_date': '1990-11-20 12:00:00'}

        with self.assertRaises(exceptions.ValidationError) as error:
            self.env['resource.model'].create(values)

        self.assertEqual(error.exception.name,
                         "The workload in week 1990, W40 is too high",
                         "Should raise exception for workload too high in week")

        values['base_workload'] = 30

        TestIntegration1.resource_2 = self.env['resource.model'].create(values)

        start_date = datetime(1990, 10, 6, 12, 0, 0)
        end_date = datetime(1990, 11, 20, 12, 0, 0)

        self.assertEqual(TestIntegration1.resource_2.project.id, TestIntegration1.project_2.id,
                         "project id doesn't match")
        self.assertEqual(TestIntegration1.resource_2.employee.id, TestIntegration1.employee_1.id,
                         "employee id doesn't match")
        self.assertEqual(TestIntegration1.resource_2.base_workload, 30, "base_workload should be 30")
        self.assertEqual(TestIntegration1.resource_2.start_date, start_date,
                         "start_date should be '1990-10-06 12:00:00'")
        self.assertEqual(TestIntegration1.resource_2.end_date, end_date, "end_date should be '1990-11-20 12:00:00'")

        for weekly_resource in TestIntegration1.resource_2.weekly_resources:
            self.assertEqual(weekly_resource.resource_id.id, TestIntegration1.resource_2.id,
                             "resource_id doesn't match")
            self.assertEqual(weekly_resource.weekly_workload, 30, "weekly_workload should be 30")

    def test_06_delete_resource(self):
        """
        Tests if creating a third resource raises a validation error because of the base workload
        being too high. Tests if deleting a resource allows the third resource to be created.

        """
        TestIntegration1.project_3 = self.env['project.project'].create({'name': 'test_project_3'})
        values = {'project': TestIntegration1.project_3.id,
                  'employee': TestIntegration1.employee_1.id,
                  'base_workload': 20,
                  'start_date': '1990-10-01 12:00:00',
                  'end_date': '1990-10-05 12:00:00'}

        with self.assertRaises(exceptions.ValidationError) as error:
            self.env['resource.model'].create(values)

        self.assertEqual(error.exception.name,
                         "The workload in week 1990, W40 is too high",
                         "Should raise exception for workload too high in week")

        resources = self.env['resource.model'].search([])
        self.assertIn(TestIntegration1.resource_2, resources)

        TestIntegration1.resource_2.unlink()

        resources = self.env['resource.model'].search([])
        self.assertNotIn(TestIntegration1.resource_2, resources)

        TestIntegration1.resource_3 = self.env['resource.model'].create(values)

        start_date = datetime(1990, 10, 1, 12, 0, 0)
        end_date = datetime(1990, 10, 5, 12, 0, 0)

        self.assertEqual(TestIntegration1.resource_3.project.id, TestIntegration1.project_3.id,
                         "project id doesn't match")
        self.assertEqual(TestIntegration1.resource_3.employee.id, TestIntegration1.employee_1.id,
                         "employee id doesn't match")
        self.assertEqual(TestIntegration1.resource_3.base_workload, 20, "base_workload should be 20")
        self.assertEqual(TestIntegration1.resource_3.start_date, start_date,
                         "start_date should be '1990-10-01 12:00:00'")
        self.assertEqual(TestIntegration1.resource_3.end_date, end_date, "end_date should be '1990-10-05 12:00:00'")

        for weekly_resource in TestIntegration1.resource_3.weekly_resources:
            self.assertEqual(weekly_resource.resource_id.id, TestIntegration1.resource_3.id,
                             "resource_id doesn't match")
            self.assertEqual(weekly_resource.weekly_workload, 20, "weekly_workload should be 20")

    def test_07_edit_weekly_resource_2(self):
        """
        Tests if editing the weekly workload of a specific weekly resource
        raises a validation error for the workload being too high.

        """
        weekly_resource = TestIntegration1.resource_3.weekly_resources[0]

        with self.assertRaises(exceptions.ValidationError) as error:
            weekly_resource.write({'weekly_workload': 50})

        self.assertEqual(error.exception.name,
                         "The workload in week 1990, W40 is too high",
                         "Should raise exception for workload too high in week")

        self.assertEqual(TestIntegration1.resource_3.base_workload, 20, "base_workload should be 20")
        self.assertEqual(weekly_resource.weekly_workload, 20, "weekly_workload should be 20")


# -------------------------------------------------------------------------------------------------------------------- #


class TestIntegration2(common.SingleTransactionCase):
    """
    This test tests a basic sequence of steps performed by a user.
    """
    project_1 = None
    project_2 = None
    employee_1 = None
    resource_1 = None
    resource_2 = None

    def test_01_create_resource_1(self):
        """
        Tests the creation of a resource.

        """
        TestIntegration2.project_1 = self.env['project.project'].create({'name': 'test_project_1'})
        TestIntegration2.employee_1 = self.env['hr.employee'].create({'name': 'test_employee_1'})
        values = {'project': TestIntegration2.project_1.id,
                  'employee': TestIntegration2.employee_1.id,
                  'base_workload': 50,
                  'start_date': '1992-03-23 12:00:00',
                  'end_date': '1992-07-17 12:00:00'}
        TestIntegration2.resource_1 = self.env['resource.model'].create(values)

        start_date = datetime(1992, 3, 23, 12, 0, 0)
        end_date = datetime(1992, 7, 17, 12, 0, 0)

        self.assertEqual(TestIntegration2.resource_1.project.id, TestIntegration2.project_1.id,
                         "project id doesn't match")
        self.assertEqual(TestIntegration2.resource_1.employee.id, TestIntegration2.employee_1.id,
                         "employee id doesn't match")
        self.assertEqual(TestIntegration2.resource_1.base_workload, 50, "base_workload should be 50")
        self.assertEqual(TestIntegration2.resource_1.start_date, start_date,
                         "start_date should be '1992-03-23 12:00:00'")
        self.assertEqual(TestIntegration2.resource_1.end_date, end_date, "end_date should be '1992-07-17 12:00:00'")

        self.assertEqual(len(TestIntegration2.resource_1.weekly_resources), 17, "Should contain 17 weekly_resources")

        for weekly_resource in TestIntegration2.resource_1.weekly_resources:
            self.assertEqual(weekly_resource.resource_id.id, TestIntegration2.resource_1.id,
                             "resource_id doesn't match")
            self.assertEqual(weekly_resource.weekly_workload, 50, "weekly_workload should be 50")

    def test_02_add_week_1(self):
        """
        Tests if adding one week to the resource works correctly.

        """
        TestIntegration2.resource_1.plus_one_week()
        self.assertEqual(len(TestIntegration2.resource_1.weekly_resources), 18, "Should contain 20 weekly_resources")

        for weekly_resource in TestIntegration2.resource_1.weekly_resources:
            self.assertEqual(weekly_resource.resource_id.id, TestIntegration2.resource_1.id,
                             "resource_id doesn't match")
            self.assertEqual(weekly_resource.weekly_workload, 50, "weekly_workload should be 50")

    def test_03_edit_weekly_resource(self):
        """
        Tests if editing the weekly workload of a weekly resource works correctly.

        """
        weekly_resource = TestIntegration2.resource_1.weekly_resources[17]
        weekly_resource.write({'weekly_workload': 30})

        self.assertEqual(TestIntegration2.resource_1.base_workload, 50, "base_workload should be 0")
        self.assertEqual(weekly_resource.weekly_workload, 30, "weekly_workload should be 30")

    def test_04_add_week_2(self):
        """
        Tests if adding one week to the resource does not affect the previously changed
        weekly workload of a weekly resource.

        """
        TestIntegration2.resource_1.plus_one_week()
        self.assertEqual(len(TestIntegration2.resource_1.weekly_resources), 19, "Should contain 20 weekly_resources")

        weekly_resources = TestIntegration2.resource_1.weekly_resources
        for i in range(0, len(weekly_resources)):
            self.assertEqual(weekly_resources[i].resource_id.id, TestIntegration2.resource_1.id,
                             "resource_id doesn't match")

            if i == 17:
                self.assertEqual(weekly_resources[i].weekly_workload, 30, "weekly_workload should be 50")
            else:
                self.assertEqual(weekly_resources[i].weekly_workload, 50, "weekly_workload should be 60")

    def test_05_create_resource_2(self):
        """
        Tests the creation of a second resource.

        """
        TestIntegration2.project_2 = self.env['project.project'].create({'name': 'test_project_2'})
        values = {'project': TestIntegration2.project_2.id,
                  'employee': TestIntegration2.employee_1.id,
                  'base_workload': 60,
                  'start_date': '1992-02-17 12:00:00',
                  'end_date': '1992-03-17 12:00:00'}
        TestIntegration2.resource_2 = self.env['resource.model'].create(values)

        start_date = datetime(1992, 2, 17, 12, 0, 0)
        end_date = datetime(1992, 3, 17, 12, 0, 0)

        self.assertEqual(TestIntegration2.resource_2.project.id, TestIntegration2.project_2.id,
                         "project id doesn't match")
        self.assertEqual(TestIntegration2.resource_2.employee.id, TestIntegration2.employee_1.id,
                         "employee id doesn't match")
        self.assertEqual(TestIntegration2.resource_2.base_workload, 60, "base_workload should be 60")
        self.assertEqual(TestIntegration2.resource_2.start_date, start_date,
                         "start_date should be '1992-02-17 12:00:00'")
        self.assertEqual(TestIntegration2.resource_2.end_date, end_date, "end_date should be '1992-03-17 12:00:00'")

        self.assertEqual(len(TestIntegration2.resource_2.weekly_resources), 5, "Should contain 5 weekly_resources")

        for weekly_resource in TestIntegration2.resource_2.weekly_resources:
            self.assertEqual(weekly_resource.resource_id.id, TestIntegration2.resource_2.id,
                             "resource_id doesn't match")
            self.assertEqual(weekly_resource.weekly_workload, 60, "weekly_workload should be 60")

    def test_06_add_week_3(self):
        """
        Tests if adding one week to the second resource raises a validation error
        because of the weekly workload being too high, since the added week is overlapping
        with the first resource.

        """
        with self.assertRaises(exceptions.ValidationError) as error:
            TestIntegration2.resource_2.plus_one_week()

        self.assertEqual(error.exception.name,
                         "The workload in week 1992, W13 is too high",
                         "Should raise exception for workload too high in week")

        self.assertEqual(len(TestIntegration2.resource_2.weekly_resources), 5, "Should contain 5 weekly_resources")

    def test_07_delete_week_1(self):
        """
        Tests if deleting one week works correctly and raises a validation error
        if the user wants to delete a week, if the resource contains only one week.

        """
        TestIntegration2.resource_2.minus_one_week()
        self.assertEqual(len(TestIntegration2.resource_2.weekly_resources), 4, "Should contain 4 weekly_resources")

        TestIntegration2.resource_2.minus_one_week()
        self.assertEqual(len(TestIntegration2.resource_2.weekly_resources), 3, "Should contain 3 weekly_resources")

        TestIntegration2.resource_2.minus_one_week()
        self.assertEqual(len(TestIntegration2.resource_2.weekly_resources), 2, "Should contain 2 weekly_resources")

        TestIntegration2.resource_2.minus_one_week()
        self.assertEqual(len(TestIntegration2.resource_2.weekly_resources), 1, "Should contain 1 weekly_resources")

        with self.assertRaises(exceptions.ValidationError) as error:
            TestIntegration2.resource_2.minus_one_week()

        self.assertEqual(error.exception.name,
                         "Start date must be before end date",
                         "Should raise exception for start date being before end date")
