from odoo import exceptions
from odoo.tests import common


class TestReportWizard(common.TransactionCase):
    """
    Test class for ReportWizard.

    Method get_report cannot be tested as it leads to a report being printed.
    """

    def test_get_weeks_1(self):
        """
        Tests whether the right data is returned by get_weeks for a timespan of 2 weeks.

        """
        w_values = {'year': 1990,
                    'week_num': 19}
        self.env['week.model'].create(w_values)

        w_values = {'year': 1990,
                    'week_num': 20}
        week1 = self.env['week.model'].create(w_values)

        w_values = {'year': 1990,
                    'week_num': 21}
        week2 = self.env['week.model'].create(w_values)

        w_values = {'year': 1990,
                    'week_num': 22}
        self.env['week.model'].create(w_values)

        values = {'start_week': week1.id,
                  'end_week': week2.id}
        wizard = self.env['resource.planning.report.wizard'].create(values)

        self.assertEqual(wizard.get_weeks(), ['1990, W20', '1990, W21'], 'Weeks should be 1990 W20 - 21')
        self.assertFalse('1990, W19' in wizard.get_weeks(), '1990 W19 should not be in result')
        self.assertFalse('1990, W22' in wizard.get_weeks(), '1990 W22 should not be in result')

    def test_get_weeks_2(self):
        """
        Tests whether the right data is returned by get_weeks for a timespan of only 1 week.

        """
        w_values = {'year': 1990,
                    'week_num': 19}
        self.env['week.model'].create(w_values)

        w_values = {'year': 1990,
                    'week_num': 20}
        week = self.env['week.model'].create(w_values)

        w_values = {'year': 1990,
                    'week_num': 21}
        self.env['week.model'].create(w_values)

        values = {'start_week': week.id,
                  'end_week': week.id}
        wizard = self.env['resource.planning.report.wizard'].create(values)

        self.assertEqual(wizard.get_weeks(), ['1990, W20'], 'Weeks should be 1990 W20')
        self.assertFalse('1990, W19' in wizard.get_weeks(), '1990 W19 should not be in result')
        self.assertFalse('1990, W21' in wizard.get_weeks(), '1990 W21 should not be in result')

    # ---------------------------------------------------------------------------------------------------------------- #
    def test_order_weeks_1(self):
        """
        Tests whether week-strings are ordered correctly
        """

        weeks = ['2020, W19', '2020, W17', '2020, W18']
        self.assertEqual(['2020, W17', '2020, W18', '2020, W19'],
                         self.env['resource.planning.report.wizard'].order_weeks(weeks),
                         'Weeks are not ordered correctly')

    def test_order_weeks_2(self):
        """
        Tests whether week-strings in correct order are not reordered
        """

        weeks = ['2020, W19', '2020, W20', '2020, W21']
        self.assertEqual(['2020, W19', '2020, W20', '2020, W21'],
                         self.env['resource.planning.report.wizard'].order_weeks(weeks),
                         'Weeks are not ordered correctly')

    def test_order_weeks_3(self):
        """
        Tests whether week-strings are ordered correctly with a timespan over new year
        """

        weeks = ['2020, W01', '2020, W02', '2019, W52']
        self.assertEqual(['2019, W52', '2020, W01', '2020, W02'],
                         self.env['resource.planning.report.wizard'].order_weeks(weeks),
                         'Weeks are not ordered correctly')
# -----------------------------------------------------------------------------------------------------------------------

    def test_start_week_before_end_week_wrong_year(self):
        """
                Tests whether it raises an error when the start_week is after the end_week
                here the year is causing the problem

        """
        start_week = self.env['week.model'].create({
            'week_num': 12,
            'year': 2021
        })
        end_week = self.env['week.model'].create({
            'week_num': 12,
            'year': 2020
        })
        values = {'start_week': start_week.id,
                  'end_week': end_week.id}

        with self.assertRaises(exceptions.ValidationError)as error:
            self.env['resource.planning.report.wizard'].create(values)
        self.assertEqual(error.exception.name,
                         "Start week must be before end week",
                         "Should raise exception if start_week is before end_week")

    def test_start_week_before_end_week_wrong_week_number(self):
        """
                     Tests whether it raises an error when the start_week is after the end_week
                     here the week number is causing the problem

        """
        start_week = self.env['week.model'].create({
            'week_num': 34,
            'year': 2020
        })
        end_week = self.env['week.model'].create({
            'week_num': 12,
            'year': 2020
        })
        values = {'start_week': start_week.id,
                  'end_week': end_week.id}

        with self.assertRaises(exceptions.ValidationError)as error:
            self.env['resource.planning.report.wizard'].create(values)
        self.assertEqual(error.exception.name,
                         "Start week must be before end week",
                         "Should raise exception if start_week is before end_week")

    def test_start_week_before_end_week_wrong_week_number_2(self):
        """
                     Tests whether it raises an error when the start_week is after the end_week
                     here the week number is causing the problem

        """
        start_week = self.env['week.model'].create({
            'week_num': 13,
            'year': 2020
        })
        end_week = self.env['week.model'].create({
            'week_num': 12,
            'year': 2020
        })
        values = {'start_week': start_week.id,
                  'end_week': end_week.id}

        with self.assertRaises(exceptions.ValidationError)as error:
            self.env['resource.planning.report.wizard'].create(values)
        self.assertEqual(error.exception.name,
                         "Start week must be before end week",
                         "Should raise exception if start_week is before end_week")

