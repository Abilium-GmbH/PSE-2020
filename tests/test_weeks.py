from odoo.tests import common
from odoo import exceptions


class TestResource(common.TransactionCase):

    def test_create_weeks_object_1(self):
        week = self.env['week.model'].create({
            'week_num': 2,
            'year': 2020
        })
        self.assertEqual(week.week_num, 2, "Week should be 2")
        self.assertEqual(week.year, 2020, "Year should be 2020")

    def test_create_weeks_object_2(self):
        week = self.env['week.model'].create({
            'week_num': 40,
            'year': 2019
        })
        self.assertNotEqual(week.week_num, 41, "Week should not be 41")
        self.assertNotEqual(week.year, 2020, "Year should not be 2020")

    def test_create_invalid_week_1(self):
        with self.assertRaises(exceptions.ValidationError):
            self.env['week.model'].create({
                'week_num': 54,
                'year': 2020
            })

    def test_create_invalid_week_2(self):
        with self.assertRaises(exceptions.ValidationError):
            self.env['week.model'].create({
                'week_num': 0,
                'year': 2020
            })
