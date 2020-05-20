from odoo import exceptions
from odoo.tests import common


class TestWeeklyResource(common.TransactionCase):
    """
    Class to test the WeeklyResource class
    """
    
    def create_resource(self):
        """
        This method is used to create a resource used for testing the weekly_resource model.
        The create method of the resource model is tested in the test_create_resource_normal method in test_resource.py
        
        :return: the resource object that will be tested 
        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 50,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}
        resource = self.env['resource.model'].create(values)
        return resource

    def test_create_weekly_resource_normal_1(self):
        """
        Tests if week_id and resource_id are stored correctly
        (part 1)
        
        :return: 
        """
        week = self.env['week.model'].create({'week_num': 30, 'year': 2020})
        resource = self.create_resource()
        weekly_resource = self.env['resource.model'].add_weekly_resource(
            {'week_id': week.id, 'resource_id': resource.id, 'weekly_workload': 50})
        self.assertEqual(weekly_resource.week_id.id, week.id, "week id doesn't match")
        self.assertEqual(weekly_resource.resource_id.id, resource.id, "resource id doesn't match")
        self.assertEqual(weekly_resource.weekly_workload, 50, "Workload doesn't match")

    def test_create_weekly_resource_normal_2(self):
        """
        Tests if week_id and resource_id are stored correctly
        (part 2, not equal to the next higher number)

        :return:
        """
        week = self.env['week.model'].create({'week_num': 30, 'year': 2020})
        resource = self.create_resource()
        weekly_resource = self.env['resource.model'].add_weekly_resource(
            {'week_id': week.id, 'resource_id': resource.id, 'weekly_workload': 50})
        self.assertNotEqual(weekly_resource.week_id.id, week.id + 1, "week id doesn't match")
        self.assertNotEqual(weekly_resource.resource_id.id, resource.id + 1, "resource id doesn't match")

    def test_create_weekly_resource_normal_3(self):
        """
        Tests if week_id and resource_id are stored correctly
        (part 3, not equal to the next lower number)

        :return:
        """
        week = self.env['week.model'].create({'week_num': 30, 'year': 2020})
        resource = self.create_resource()
        weekly_resource = self.env['resource.model'].add_weekly_resource(
            {'week_id': week.id, 'resource_id': resource.id, 'weekly_workload': 50})
        self.assertNotEqual(weekly_resource.week_id.id, week.id - 1, "week id doesn't match")
        self.assertNotEqual(weekly_resource.resource_id.id, resource.id - 1, "resource id doesn't match")

    def test_edit_weekly_resource_1(self):
        """
        Test editing the weekly_workload.

        :return:
        """
        week = self.env['week.model'].create({'week_num': 30, 'year': 2020})
        resource = self.create_resource()
        weekly_resource = self.env['resource.model'].add_weekly_resource(
            {'week_id': week.id, 'resource_id': resource.id, 'weekly_workload': 50})

        weekly_resource.write({'week_id': week.id, 'resource_id': resource.id, 'weekly_workload': 70})

        self.assertEqual(weekly_resource.weekly_workload, 70, 'weekly_workload should be 70')

    def test_edit_weekly_resource_2(self):
        """
        Test if editing weekly_workload raises an error
        if weekly_workload is larger than 100.

        :return:
        """
        week = self.env['week.model'].create({'week_num': 30, 'year': 2020})
        resource = self.create_resource()
        weekly_resource = self.env['resource.model'].add_weekly_resource(
            {'week_id': week.id, 'resource_id': resource.id, 'weekly_workload': 20})

        with self.assertRaises(exceptions.ValidationError) as error:
            weekly_resource.write({'week_id': week.id, 'resource_id': resource.id, 'weekly_workload': 110})

        self.assertEqual("The given workload can't be larger than 100", error.exception.name, 'Error does not match')

    def test_edit_weekly_resource_3(self):
        """
        Test if editing weekly_workload raises an error
        if weekly_workload is smaller than 0.

        :return:
        """
        week = self.env['week.model'].create({'week_num': 30, 'year': 2020})
        resource = self.create_resource()
        weekly_resource = self.env['resource.model'].add_weekly_resource(
            {'week_id': week.id, 'resource_id': resource.id, 'weekly_workload': 70})

        with self.assertRaises(exceptions.ValidationError) as error:
            weekly_resource.write({'week_id': week.id, 'resource_id': resource.id, 'weekly_workload': -10})

        self.assertEqual("The given workload can't be smaller than 0", error.exception.name, 'Error does not match')

    def test_edit_weekly_resource_4(self):
        """
        Test if editing weekly_workload so that the total workload of a employee
        in a week is larger than 100 raises an error.

        :return:
        """
        week = self.env['week.model'].create({'week_num': 40, 'year': 2020})
        resource = self.create_resource()
        weekly_resource1 = self.env['resource.model'].add_weekly_resource(
            {'week_id': week.id, 'resource_id': resource.id, 'weekly_workload': 70})

        weekly_resource2 = self.env['resource.model'].add_weekly_resource(
            {'week_id': week.id, 'resource_id': resource.id, 'weekly_workload': 20})

        with self.assertRaises(exceptions.ValidationError) as error:
            weekly_resource2.write({'week_id': week.id, 'resource_id': resource.id, 'weekly_workload': 40})

        self.assertEqual("The workload in week " + week.week_string + " is too high", error.exception.name,
                         'Error does not match')
