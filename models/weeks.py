from odoo import models, fields

class Weeks(models.Model):
    _name = "week.model"
    week_num = fields.Integer(string='Wochennummer')


    def add_weeks(self):
        vals = {'week_num': 1}
        self.create_weeks(vals)

