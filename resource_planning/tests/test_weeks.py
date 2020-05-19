from datetime import datetime,timedelta

from odoo.tests import common
from odoo import exceptions


class TestWeeks(common.TransactionCase):
    """
    Class to test the Weeks class

    The method is_in_week_period() gets not tested because it uses todays date
    and only gets the week_delta parameter. The called method set_is_week_in_period where most logic is
    gets tested
    """

    def test_create_weeks_object_1(self):
        """
        Tests the creating of a single week object

        :return:
        """
        week = self.env['week.model'].create({
            'week_num': 2,
            'year': 2020
        })
        self.assertEqual(week.week_num, 2, "Week should be 2")
        self.assertEqual(week.year, 2020, "Year should be 2020")

    def test_create_weeks_object_2(self):
        """
        Tests the creating of a second week object

        :return:
        """
        week = self.env['week.model'].create({
            'week_num': 40,
            'year': 2019
        })
        self.assertNotEqual(week.week_num, 41, "Week should not be 41")
        self.assertNotEqual(week.year, 2020, "Year should not be 2020")

    def test_create_invalid_week_1(self):
        """
        Tests if exception is raised when creating an invalid week
        Week number too high

        :return:
        """
        with self.assertRaises(exceptions.ValidationError):
            self.env['week.model'].create({
                'week_num': 54,
                'year': 2020
            })

    def test_create_invalid_week_2(self):
        """
        Tests if exception is raised when creating an invalid week
        Week number too low

        :return:
        """
        with self.assertRaises(exceptions.ValidationError):
            self.env['week.model'].create({
                'week_num': 0,
                'year': 2020
            })

#-----------------------------------------------------------------------------------------------------------------------
    def test_name_get(self):
        """
        tests if name is created correctly
        """
        week = self.env['week.model'].create({
            'week_num': 2,
            'year': 2020
        })
        self.assertEqual(week.name_get()[0][1], 'Week 2 2020', "Week string should be Week 2")

    def test_name_get_2(self):
        """
                tests if name is created correctly
        """
        week = self.env['week.model'].create({
            'week_num': 4,
            'year': 2020
        })
        self.assertNotEqual(week.name_get()[0][1], 'Week 2 2020', "Week string should be Week 4 and not 2")

    def test_name_get_3(self):
        """
                tests if name is created correctly and whitespace is correct
        """
        week = self.env['week.model'].create({
            'week_num': 2,
            'year': 2020
        })
        self.assertNotEqual(week.name_get()[0][1], 'Week  2 2020',
                            "Week string should be Week 2, one white space too much")

    def test_name_get_incorrect_year(self):
        """
                tests if name is created correctly and year is correct
        """
        week = self.env['week.model'].create({
            'week_num': 2,
            'year': 2021
        })
        self.assertNotEqual(week.name_get()[0][1], 'Week 2 2020', "Week string should be Week 2")
        self.assertEqual(week.name_get()[0][1], 'Week 2 2021', "Week string should be Week 2")

# -----------------------------------------------------------------------------------------------------------------------
    def test_set_is_week_in_period_week_bool_true(self):
        """
                    tests if week_bool is set to true with a
                    week_delta of 8
        """
        today = datetime(2020, 5, 10, 13, 42, 7)
        this_week = today - timedelta(today.weekday())
        self.env['week.model'].create({
            'week_num': 20,
            'year': 2020
        })
        self.env['week.model'].create({
            'week_num': 21,
            'year': 2020
        })

        self.env['week.model'].set_is_week_in_period(this_week, 8)
        for week in self.env['week.model']:
            self.assertTrue(week.week_bool, "Week_bool is true therefore week is after this week")

    def test_set_is_week_in_period_week_bool_false(self):
        """
                tests if week_bool is set to false with a
                week_delta of 8
        """
        today = datetime(2020, 5, 10, 13, 42, 7)
        this_week = today - timedelta(today.weekday())
        self.env['week.model'].create({
            'week_num': 19,
            'year': 2020
        })
        self.env['week.model'].create({
            'week_num': 18,
            'year': 2020
        })

        self.env['week.model'].set_is_week_in_period(this_week, 8)
        if self.env['week.model'].week_num == 14:
            self.assertFalse(self.env['week.model'].week_bool, "Week_bool is false therefore week is before this week")

    def test_set_is_week_in_period_week_bool_mixed(self):
        """
            tests if week_bool is set to false for week 18 and true for week 19 with a
            week_delta of 8
        """
        today = datetime(2020, 5, 10, 13, 42, 7)
        this_week = today - timedelta(today.weekday())
        self.env['week.model'].create({
            'week_num': 18,
            'year': 2020
        })
        self.env['week.model'].create({
            'week_num': 19,
            'year': 2020
        })
        self.env['week.model'].set_is_week_in_period(this_week,8)

        for week in self.env['week.model']:
            if week.week_num == 18:
                self.assertFalse(week.week_bool,"Week_bool is false therefore week is before this week")
            else:
                self.assertTrue(week.week_bool,
                                 "Week_bool is true therefore week is after this week")

    def test_set_is_week_in_period_week_bool_false_over_year_bound(self):
        """
                   tests if week_bool is set to false with a
                   week_delta of 8 and whether it works of the year bound
        """
        today = datetime(2021, 12, 23, 13, 42, 7)
        this_week = today - timedelta(today.weekday())
        self.env['week.model'].create({
            'week_num': 52,
            'year': 2020
        })
        self.env['week.model'].create({
            'week_num': 1,
            'year': 2020
        })
        self.env['week.model'].set_is_week_in_period(this_week,8)
        for week in self.env['week.model']:
            self.assertFalse(week.week_bool, "Week_bool is false therefore week is before this week")

    def test_set_is_week_in_period_week_bool_true_over_year_bound(self):
        """
                tests if week_bool is set to true with a
                week_delta of 8 and whether it works of the year bound
        """
        today = datetime(2020, 12, 23, 13, 42, 7)
        this_week = today - timedelta(today.weekday())
        self.env['week.model'].create({
            'week_num': 52,
            'year': 2020
        })
        self.env['week.model'].create({
            'week_num': 1,
            'year': 2021
        })
        self.env['week.model'].set_is_week_in_period(this_week,8)
        for week in self.env['week.model']:
            self.assertTrue(week.week_bool, "Week_bool is true therefore week is after this week")

    def test_set_is_week_in_period_week_bool_true_going_backwards(self):
        """
                tests if week_bool is set to true when week delta is negative

        """
        today = datetime(2020, 11, 9, 13, 42, 7)
        this_week = today - timedelta(today.weekday())
        self.env['week.model'].create({
            'week_num': 44,
            'year': 2020
        })
        self.env['week.model'].create({
            'week_num': 45,
            'year': 2020
        })
        self.env['week.model'].create({
            'week_num': 46,
            'year': 2020
        })
        self.env['week.model'].set_is_week_in_period(this_week,-2)
        for week in self.env['week.model']:
            self.assertTrue(week.week_bool, "Week_bool is true therefore week is before this week, because week delta is negative")

    def test_set_is_week_in_period_week_bool_true_week_delta_zero(self):
        """
                 tests if week_bool is set to true when week delta is 0, only the current week should be seen

        """
        today = datetime(2020, 11, 9, 13, 42, 7)
        this_week = today - timedelta(today.weekday())
        self.env['week.model'].create({
            'week_num': 46,
            'year': 2020
        })
        self.env['week.model'].create({
            'week_num': 47,
            'year': 2020
        })
        self.env['week.model'].set_is_week_in_period(this_week, 0)
        for week in self.env['week.model']:
            if week.week_num == 46:
                self.assertTrue(week.week_bool, "Week_bool is true therefore week is before this week, because"
                                                        " week delta is 0")
            else:
                self.assertFalse(week.week_bool,
                             "Week_bool is false, week delta is 0 ")

    def test_set_is_week_in_period_week_bool_false_going_backwards(self):
        """
                tests if week_bool is set to false when week delta is negative
        """
        today = datetime(2020, 11, 30, 13, 42, 7)
        this_week = today - timedelta(today.weekday())
        self.env['week.model'].create({
            'week_num': 44,
            'year': 2020
        })
        self.env['week.model'].create({
            'week_num': 45,
            'year': 2020
        })
        self.env['week.model'].create({
            'week_num': 46,
            'year': 2020
        })
        self.env['week.model'].set_is_week_in_period(this_week,-2)
        for week in self.env['week.model']:
            self.assertFalse(week.week_bool, "Week_bool is false therefore week is after this week, weeks are"
                                                    " even further back")

    def test_set_is_week_in_period_week_bool_mixed_going_backwards(self):
        """
                tests if week_bool is set to false for week 46 and true for 44 and 45 when week delta is negative
        """
        today = datetime(2020, 11, 3, 13, 42, 7)
        this_week = today - timedelta(today.weekday())
        self.env['week.model'].create({
            'week_num': 44,
            'year': 2020
        })
        self.env['week.model'].create({
            'week_num': 45,
            'year': 2020
        })
        self.env['week.model'].create({
            'week_num': 46,
            'year': 2020
        })
        self.env['week.model'].set_is_week_in_period(this_week, -2)
        for week in self.env['week.model']:
            if week.week_num == 46:
                self.assertFalse(week.week_bool, "Week_bool is false, week is after this week")
            else:
                self.assertTrue(week.week_bool,
                                 "Week_bool is true therefore week is before this week, lies within week delta")

    def test_set_is_week_in_period_mixed_going_backwards_over_year_bound(self):
        """
             tests if week_bool is set to false for week 52 and true for 1 and 2 when week delta is negative
        """
        today = datetime(2021, 1, 5, 13, 42, 7)
        this_week = today - timedelta(today.weekday())
        self.env['week.model'].create({
            'week_num': 52,
            'year': 2020
        })
        self.env['week.model'].create({
            'week_num': 1,
            'year': 2021
        })
        self.env['week.model'].create({
            'week_num': 2,
            'year': 2021
        })
        self.env['week.model'].set_is_week_in_period(this_week, -1)
        for week in self.env['week.model']:
            if week.week_num == 52:
                self.assertFalse(week.week_bool, "Week_bool is false because week is too far in the past")
            else:
                self.assertTrue(week.week_bool,
                                 "Week_bool is true therefore week is before this week, lies within week delta")

