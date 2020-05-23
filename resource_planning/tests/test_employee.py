from odoo.tests import common


class TestEmployee(common.TransactionCase):
    """
    Class to test the Employee class
    """

    def test_compute_total_workload_1(self):
        """
        Tests if total workload is computed correctly for 2 weeks

        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 50,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}
        resource1 = self.env['resource.model'].create(values)
        week_model14 = self.env['week.model'].search([['week_num', '=', 14], ['year', '=', 2020]])
        week_model15 = self.env['week.model'].search([['week_num', '=', 15], ['year', '=', 2020]])

        values2 = {'project': project.id,
                   'employee': employee.id,
                   'base_workload': 30,
                   'start_date': '2020-04-06 13:42:07',
                   'end_date': '2020-04-12 13:42:07'}
        resource2 = self.env['resource.model'].create(values2)

        total_workload_week_14 = employee.compute_total_workload(week_model14)
        total_workload_week_15 = employee.compute_total_workload(week_model15)

        self.assertEqual(total_workload_week_14, 50, "Total workload in week 14 should be 50 %")
        self.assertEqual(total_workload_week_15, 80, "Total workload in week 15 should be 80 %")

    def test_compute_total_workload_2(self):
        """
        Tests if total workload is computed correctly for 3 weeks

        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 30,
                  'start_date': '2020-04-05 13:42:07',
                  'end_date': '2020-04-12 13:42:07'}
        resource1 = self.env['resource.model'].create(values)
        week_model14 = self.env['week.model'].search([['week_num', '=', 14], ['year', '=', 2020]])
        week_model15 = self.env['week.model'].search([['week_num', '=', 15], ['year', '=', 2020]])

        values2 = {'project': project.id,
                   'employee': employee.id,
                   'base_workload': 70,
                   'start_date': '2020-04-06 13:42:07',
                   'end_date': '2020-04-19 13:42:07'}
        resource2 = self.env['resource.model'].create(values2)
        week_model16 = self.env['week.model'].search([['week_num', '=', 16], ['year', '=', 2020]])

        total_workload_week_14 = employee.compute_total_workload(week_model14)
        total_workload_week_15 = employee.compute_total_workload(week_model15)
        total_workload_week_16 = employee.compute_total_workload(week_model16)

        self.assertEqual(total_workload_week_14, 30, "Total workload in week 14 should be 30 %")
        self.assertEqual(total_workload_week_15, 100, "Total workload in week 15 should be 100 %")
        self.assertEqual(total_workload_week_16, 70, "Total workload in week 16 should be 70 %")

    def test_compute_total_workload_3(self):
        """
        Tests if total workload is computed correctly for 2 weeks over year bounds

        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        values = {'project': project.id,
                  'employee': employee.id,
                  'base_workload': 20,
                  'start_date': '2020-12-28 13:42:07',
                  'end_date': '2021-01-08 13:42:07'}
        self.env['resource.model'].create(values)
        week_model53 = self.env['week.model'].search([['week_num', '=', 53], ['year', '=', 2020]])
        week_model1 = self.env['week.model'].search([['week_num', '=', 1], ['year', '=', 2021]])

        values2 = {'project': project.id,
                   'employee': employee.id,
                   'base_workload': 70,
                   'start_date': '2021-01-04 13:42:07',
                   'end_date': '2021-01-12 13:42:07'}
        self.env['resource.model'].create(values2)
        week_model2 = self.env['week.model'].search([['week_num', '=', 2], ['year', '=', 2021]])

        total_workload_week_53 = employee.compute_total_workload(week_model53)
        total_workload_week_1 = employee.compute_total_workload(week_model1)
        total_workload_week_2 = employee.compute_total_workload(week_model2)

        self.assertEqual(total_workload_week_53, 20, "Total workload in week 53 should be 20 %")
        self.assertEqual(total_workload_week_1, 90, "Total workload in week 1 should be 90 %")
        self.assertEqual(total_workload_week_2, 70, "Total workload in week 2 should be 70 %")
