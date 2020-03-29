from odoo import models, fields


# TODO: Optimize week-representation (e.g. yyyy, W+weekNumber) --> Add field?
class Weeks(models.Model):
    _name = "week.model"
    week_num = fields.Integer(string='Week')
    year = fields.Integer(string="Year")



