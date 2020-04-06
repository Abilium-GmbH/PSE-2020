from odoo import exceptions
from odoo.tests import common


class TestWeeklyResource(common.TransactionCase):

    # this method is used to create a resource used for testing the weekly_resource model
    # The create method of the resource model is tested in the test_create_resource_normal method in test_resource.py
    def create_resource(self):
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'workload': 50,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}
        resource = self.env['resource.model'].create(values)
        return resource

    def test_create_weekly_resource_normal_1(self):
        week = self.env['week.model'].create({'week_num': 30, 'year': 2020})
        resource = self.create_resource()
        weekly_resource = self.env['resource.model'].add_weekly_resource(
            {'week_id': week.id, 'resource_id': resource.id})
        self.assertEqual(weekly_resource.week_id.id, week.id, "week id doesn't match")
        self.assertEqual(weekly_resource.resource_id.id, resource.id, "resource id doesn't match")

    def test_create_weekly_resource_normal_2(self):
        week = self.env['week.model'].create({'week_num': 30, 'year': 2020})
        resource = self.create_resource()
        weekly_resource = self.env['resource.model'].add_weekly_resource(
            {'week_id': week.id, 'resource_id': resource.id})
        self.assertNotEqual(weekly_resource.week_id.id, week.id + 1, "week id doesn't match")
        self.assertNotEqual(weekly_resource.resource_id.id, resource.id + 1, "resource id doesn't match")

    def test_create_weekly_resource_normal_3(self):
        week = self.env['week.model'].create({'week_num': 30, 'year': 2020})
        resource = self.create_resource()
        weekly_resource = self.env['resource.model'].add_weekly_resource(
            {'week_id': week.id, 'resource_id': resource.id})
        self.assertNotEqual(weekly_resource.week_id.id, week.id - 1, "week id doesn't match")
        self.assertNotEqual(weekly_resource.resource_id.id, resource.id - 1, "resource id doesn't match")
