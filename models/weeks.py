from odoo import models, fields, api, exceptions


class Weeks(models.Model):
    _name = "week.model"
    week_num = fields.Integer(string='Week', required=True)
    year = fields.Integer(string="Year", required=True)
    week_string = fields.Char(string="Week String", compute='get_week_string', store=True)

    @api.depends('year', 'week_num')
    def get_week_string(self):
        for s in self:
            string = str(s.year) + ', W' + str(s.week_num)
            s.week_string = string
        return 0

    @api.constrains('week_num')
    def _check_if_week_num_is_valid(self):
        for r in self:
            if r.week_num < 1:
                raise exceptions.ValidationError("Week Number can't be smaller than 1")
            elif r.week_num > 53:
                raise exceptions.ValidationError("Week Number can't be bigger than 52")
