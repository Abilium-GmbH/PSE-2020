from datetime import datetime
from odoo import exceptions, models
from odoo.tests import common


class TestWorkload(common.SavepointCase):

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

        :return:
        """
        values = {'project': TestWorkload.project.id,
                  'employee': TestWorkload.employee.id,
                  'base_workload': 50,
                  'start_date': '2020-04-06 13:42:07',
                  'end_date': '2020-04-10 13:42:07'}
        resource = self.env['resource.model'].create(values)

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

        :return:
        """
        values = {'project': TestWorkload.project.id,
                  'employee': TestWorkload.employee.id,
                  'base_workload': 40,
                  'start_date': '2020-04-13 13:42:07',
                  'end_date': '2020-04-22 13:42:07'}
        resource = self.env['resource.model'].create(values)

        values = {'project': TestWorkload.project.id,
                  'employee': TestWorkload.employee.id,
                  'base_workload': 60,
                  'start_date': '2020-04-21 13:42:07',
                  'end_date': '2020-04-30 13:42:07'}
        resource = self.env['resource.model'].create(values)

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

        :return:
        """
        values = {'project': TestWorkload.project.id,
                  'employee': TestWorkload.employee.id,
                  'base_workload': 40,
                  'start_date': '2020-05-05 13:42:07',
                  'end_date': '2020-05-08 13:42:07'}
        resource = self.env['resource.model'].create(values)

        values = {'project': TestWorkload.project.id,
                  'employee': TestWorkload.employee.id,
                  'base_workload': 60,
                  'start_date': '2020-05-18 13:42:07',
                  'end_date': '2020-05-29 13:42:07'}
        resource = self.env['resource.model'].create(values)

        values = {'project': TestWorkload.project.id,
                  'employee': TestWorkload.employee.id,
                  'base_workload': 50,
                  'start_date': '2020-05-04 13:42:07',
                  'end_date': '2020-05-22 13:42:07'}

        with self.assertRaises(exceptions.ValidationError)as error:
            self.env['resource.model'].create(values)

        self.assertEqual(error.exception.name,
                         "The workload in week 2020, W21 is too high", "Should raise exception for Workload too high")
