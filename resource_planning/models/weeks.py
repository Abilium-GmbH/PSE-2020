from datetime import timedelta, date

from odoo import models, fields, api, exceptions


class Weeks(models.Model):
    """
    A class used to represent a specific week in a specific year

    :param week_num: the calendaric number of the week in the year, is required
    :param year: the year, is required
    :param week_string: the representation of week and year for the view
    :param week_bool: is True if the week number is within the next two months otherwise False
     :param week_delta: given by the user how many weeks he wants to see
    """
    _name = "week.model"
    _description = "Week"
    week_num = fields.Integer(string='Week', required=True)
    year = fields.Integer(string="Year", required=True)
    week_string = fields.Char(string="Week String", compute='get_week_string', store=True)
    week_bool = fields.Boolean(compute="is_week_in_period", string="is week in the weeks definded by settings", store=True)
    week_delta = fields.Integer(default=8)

    def name_get(self):
        result = []
        for record in self:
            record_name = 'Week' + '   ' + str(record.week_num)
            result.append((record.id, record_name))
        return result

    @api.depends('week_delta')
    def is_week_in_period(self):
        """
              calculates current week and calls set_is_week_in_period
              :param week_delta is needed for set_is_week_in_period
        """
        today = date.today()
        this_week = today - timedelta(today.weekday())
        self.set_is_week_in_period(this_week)

    @api.depends('week_delta')
    def set_is_week_in_period(self, this_week):
        """
        sets week_bool whether the week is in the period the user wants or not (true or false)
        :returns week_bool
        :param week_delta is needed to find the last week
        :param this_week which is the current week number
        """

        for week in self:
            year = week.year
            temp = date(year, 1, 1)
            temp = temp - timedelta(temp.weekday())
            delta = timedelta(days=(week.week_num - 1) * 7)
            start_date_of_week = temp + delta

            if week.week_delta >= 0:
                if this_week + timedelta(
                        weeks=week.week_delta) >= start_date_of_week and this_week <= start_date_of_week:
                    week.week_bool = True
                else:
                    week.week_bool = False
            else:
                if this_week + timedelta(
                        weeks=week.week_delta) <= start_date_of_week and this_week >= start_date_of_week:
                    week.week_bool = True
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
