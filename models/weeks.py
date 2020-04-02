from odoo import models, fields, api, exceptions


# TODO: Optimize week-representation (e.g. yyyy, W+weekNumber) --> Add field?
class Weeks(models.Model):
    _name = "week.model"
    week_num = fields.Integer(string='Week', required=True)
    year = fields.Integer(string="Year", required=True)

    @api.constrains('week_num')
    def _check_if_week_num_is_valid(self):
        for r in self:
            if r.week_num < 1:
                raise exceptions.ValidationError("Week Number can't be smaller than 1")
            elif r.week_num > 53:
                raise exceptions.ValidationError("Week Number can't be bigger than 52")
