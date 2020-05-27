from odoo.tests import common


class TestReportView(common.TransactionCase):
    """
        Test class for ReportView
        Tests whether the required data for the report is computed correctly

    """

    def test_is_relevant_1(self):
        """
        Tests, whether a week_array of relevant week_data's is considered relevant.

        """
        model = self.env['report.resource_planning_report.planning_report_view']
        week_array = []
        week_data_1 = {'week': '2020, W20',
                       'workload': 20}
        week_data_2 = {'week': '2020, W21',
                       'workload': 20}
        week_data_3 = {'week': '2020, W22',
                       'workload': 20}
        week_array.append(week_data_1)
        week_array.append(week_data_2)
        week_array.append(week_data_3)

        self.assertTrue(model.is_relevant(week_array), 'week_array should be relevant')

    def test_is_relevant_2(self):
        """
        Tests, whether a week_array of mainly relevant week_data's is considered relevant.

        """

        model = self.env['report.resource_planning_report.planning_report_view']
        week_array = []
        week_data_1 = {'week': '2020, W20',
                       'workload': 0}
        week_data_2 = {'week': '2020, W21',
                       'workload': 20}
        week_data_3 = {'week': '2020, W22',
                       'workload': 20}
        week_array.append(week_data_1)
        week_array.append(week_data_2)
        week_array.append(week_data_3)

        self.assertTrue(model.is_relevant(week_array), 'week_array should be relevant')

    def test_is_relevant_3(self):
        """
        Tests, whether a week_array with only one relevant week_data is considered relevant.

        """

        model = self.env['report.resource_planning_report.planning_report_view']
        week_array = []
        week_data_1 = {'week': '2020, W20',
                       'workload': 0}
        week_data_2 = {'week': '2020, W21',
                       'workload': 0}
        week_data_3 = {'week': '2020, W22',
                       'workload': 20}
        week_array.append(week_data_1)
        week_array.append(week_data_2)
        week_array.append(week_data_3)

        self.assertTrue(model.is_relevant(week_array), 'week_array should be relevant')

    def test_is_not_relevant(self):
        """
        Tests, whether a week_array with only irrelevant week_data's is considered irrelevant.

        """

        model = self.env['report.resource_planning_report.planning_report_view']
        week_array = []
        week_data_1 = {'week': '2020, W20',
                       'workload': 0}
        week_data_2 = {'week': '2020, W21',
                       'workload': 0}
        week_data_3 = {'week': '2020, W22',
                       'workload': 0}
        week_array.append(week_data_1)
        week_array.append(week_data_2)
        week_array.append(week_data_3)

        self.assertFalse(model.is_relevant(week_array), 'week_array should be relevant')

    # ---------------------------------------------------------------------------------------------------------------- #

    def test_get_report_values_1(self):
        """
        Tests whether _get_report_values creates the correct report data.

        If this test fails, there weekly_resource records that were planned during the
        tested timespan (1990, W19-21) in your database.

        """
        project = self.env['project.project'].create({'name': 'p1'})
        employee = self.env['hr.employee'].create({'name': 'e1'})
        r_values = {'project': project.id,
                    'employee': employee.id,
                    'base_workload': 50,
                    'start_date': '1990-05-07 13:42:07',
                    'end_date': '1990-05-13 13:42:07'}
        self.env['resource.model'].create(r_values)

        data = {'model': 'resource.planning.report.wizard',
                'ids': 1,
                'form': {
                    'weeks': ['1990, W19', '1990, W20', '1990, W21']
                }}
        docs = self.env['report.resource_planning_report.planning_report_view']._get_report_values(self, data)

        self.assertEqual(docs['doc_ids'], 1, 'Id should be 1')
        self.assertEqual(docs['doc_model'], 'resource.planning.report.wizard', 'Model should be report wizard')
        self.assertEqual(docs['weeks'], ['1990, W19', '1990, W20', '1990, W21'], 'Weeks should be 1990 W19 - W21')
        self.assertEqual(docs['docs'],
                         [{'project': 'p1',
                           'employee': 'e1',
                           'weekly_data': [{'week': '1990, W19', 'workload': 50},
                                           {'week': '1990, W20', 'workload': 0},
                                           {'week': '1990, W21', 'workload': 0}]},
                          {'project': ' ',
                           'employee': 'Total',
                           'weekly_data': [{'week': '1990, W19', 'workload': 50},
                                           {'week': '1990, W20', 'workload': 0},
                                           {'week': '1990, W21', 'workload': 0}]}], 'Report data not correct')

    def test_get_report_values_2(self):
        """
        Tests whether _get_report_values creates the correct report data if there aren't any weekly_resources
        in the tested timespan.

        If this test fails, there are weekly_resource records planned during the tested timespan (1990, W19-21)
        in your database.

        """
        w_values = {'year': 1990,
                    'week_num': 19}
        self.env['week.model'].create(w_values)
        w_values = {'year': 1990,
                    'week_num': 20}
        self.env['week.model'].create(w_values)
        w_values = {'year': 1990,
                    'week_num': 21}
        self.env['week.model'].create(w_values)

        data = {'model': 'resource.planning.report.wizard',
                'ids': 1,
                'form': {
                    'weeks': ['1990, W19', '1990, W20', '1990, W21']
                }}
        docs = self.env['report.resource_planning_report.planning_report_view']._get_report_values(self, data)

        self.assertEqual(docs['doc_ids'], 1, 'Id should be 1')
        self.assertEqual(docs['doc_model'], 'resource.planning.report.wizard', 'Model should be report wizard')
        self.assertEqual(docs['weeks'], ['1990, W19', '1990, W20', '1990, W21'], 'Weeks should be 1990 W19 - W21')
        self.assertEqual(docs['docs'], [{'project': ' ',
                                         'employee': 'Total',
                                         'weekly_data': [{'week': '1990, W19', 'workload': 0},
                                                         {'week': '1990, W20', 'workload': 0},
                                                         {'week': '1990, W21', 'workload': 0}]}],
                         'Report data not correct')
