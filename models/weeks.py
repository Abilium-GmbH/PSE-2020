from odoo import models, fields, api, exceptions


class Weeks(models.Model):
    """
    A class used to represent a specific week in a specific year

    :param week_num: the calendaric number of the week in the year, is required
    :param year: the year, is required
    :param week_string: the representation of week and year for the view
    :param week_bool: is True if the week number is within the next two months otherwise False
    :param week_num_in_two_months: week number in two months current week number + 8 weeks
    """
    _name = "week.model"
    _description = "Week"
    week_num = fields.Integer(string='Week', required=True)
    year = fields.Integer(string="Year", required=True)
    week_string = fields.Char(string="Week String", compute='get_week_string', store=True)
    week_bool = fields.Boolean(compute="is_week_in_next_2_months", string="is week in next two Months", store=True)
    week_num_in_two_months = fields.Integer(compute="get_week_num_in_two_months", string="Week number in 2 Months")

    @api.depends('week_num_in_two_months')
    def get_week_num_in_two_months(self):
        """
        gets week number which is 2 months in the future
        :returns assigns result directly to week_num_in_two_months
                """
        self.week_num_in_two_months = fields.Date.today().isocalendar()[1] + 8

    @api.depends('week_num', 'week_bool')
    def is_week_in_next_2_months(self):
        """
            calculates for every week whether it is in the next 2 months starting from
            this week
            :returns sets week_bool to TRUE or FALSE
         """
        for week in self:
            if fields.Date.today().isocalendar()[1] + 8 - week.week_num >= 0:
                if fields.Date.today().isocalendar()[1] - week.week_num <= 0:
                    week.week_bool = True
                else:
                    week.week_bool = False
            else:
                week.week_bool = False

    @api.depends('year', 'week_num')
    def get_week_string(self):
        """
        Builds and stores the week_string attribute
        based on year and week_num with a 'W' prefix, seperated by a comma

        :return: 0
        """
        for s in self:
            string = str(s.year) + ', W'
            if s.week_num < 10:
                string = string + "0" + str(s.week_num)
            else:
                string = string + str(s.week_num)
            s.week_string = string
        return 0

    @api.constrains('week_num')
    def _check_if_week_num_is_valid(self):
        """
        Checks if the week_num is within the valid range from 1 to 53

        :raises:
            :exception ValidationError: if week_num < 1 or week_num > 53
        :return: no return value
        """
        for r in self:
            if r.week_num < 1:
                raise exceptions.ValidationError("Week Number can't be smaller than 1")
            elif r.week_num > 53:
                raise exceptions.ValidationError("Week Number can't be bigger than 53")
