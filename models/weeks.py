from odoo import models, fields

class Weeks(models.Model):
    _name = "week.model"
    week_num = fields.Integer(string='Week')
    year = fields.Integer(string="Year")

    def add_weeks(self):
        vals = {'week_num': 1, 'year': 2}
        self.create_weeks(vals)

