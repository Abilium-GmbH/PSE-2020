from odoo import models, fields, api, exceptions


class Weeks(models.Model):
    """
    A class used to represent a specific week in a specific year
    :param week_num: the calendaric number of the week in the year, is required
    :param year: the year, is required
    :param week_string: the representation of week and year for the view
    """
    _name = "week.model"
    week_num = fields.Integer(string='Week', required=True)
    year = fields.Integer(string="Year", required=True)
    week_string = fields.Char(string="Week String", compute='get_week_string', store=True)

    @api.depends('year', 'week_num')
    def get_week_string(self):
        """
        builds and stores the week_string attribute
        based on year and week_num with a 'W' prefix, seperated by a comma
        :return: 0
        """
        for s in self:
            string = str(s.year) + ', W' + str(s.week_num)
            s.week_string = string
        return 0

    @api.constrains('week_num')
    def _check_if_week_num_is_valid(self):
        """
        checks if the week_num is within the valid range from 1 to 53
        :raises:
            :exception ValidationError: if week_num < 1 or week_num > 53
        :return: no return value
        """
        for r in self:
            if r.week_num < 1:
                raise exceptions.ValidationError("Week Number can't be smaller than 1")
            elif r.week_num > 53:
                raise exceptions.ValidationError("Week Number can't be bigger than 53")
