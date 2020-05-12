from datetime import datetime, timedelta
from odoo import exceptions
from odoo.tests import common
from psycopg2 import errors


class TestReportView(common.TransactionCase):

    def test_is_relevant_1(self):
        """
        Tests, whether a week_array of relevant week_data's is considered relevant

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
        Tests, whether a week_array of mainly relevant week_data's is considered relevant

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
        Tests, whether a week_array with only one relevant week_data is considered relevant

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
        Tests, whether a week_array with only irrelevant week_data's is considered irrelevant

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