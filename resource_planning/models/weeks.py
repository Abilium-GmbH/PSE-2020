import datetime
from datetime import timedelta, date

from odoo import models, fields, api, exceptions


class Weeks(models.Model):
    """
    Represents a specific week in a specific year, defined by variables week_num and year.
    Stores also other variables used in the module:

    # week_string to represent a week_model in the UI

    # week_bool to declare whether a week is in the timespan defined by res_config_settings.

    """
    _name = "week.model"
    _description = "Week"
    _order = "week_num asc"
    week_num = fields.Integer(string='Week', required=True)
    year = fields.Integer(string="Year", required=True)
    week_string = fields.Char(string="Week String", compute='build_week_string', store=True)
    week_bool = fields.Boolean(compute="is_week_in_period", string="is week in the weeks definded by settings",
                               store=True)

    @api.model
    def create(self, values):
        """
        Constructor
        calls is_week_in_period to set the week_bool
        :param values: the values used to create the week model

        :return: the created record
        """
        rec = super(Weeks, self).create(values)

        rec.is_week_in_period()

        return rec

    def name_get(self):
        """
         Creates a String representation which is used for the report view
         :return: String representation
        """
        result = []
        for record in self:
            record_name = 'Week' + ' ' + str(record.week_num) + ' ' + str(record.year)
            result.append((record.id, record_name))
        return result

    def is_week_in_period(self):
        """
        Calculates the current week and calls set_is_week_in_period
        Gets week_delta (number of weeks one would like to see in the filter) from ir.config_parameter
        Called daily so filter is up to date
        :return: week_delta
        """
        today = datetime.datetime.today()
        week_delta = int(self.env['ir.config_parameter'].sudo().get_param('resource_planning.filter_weeks'))
        this_week_uncut = today - datetime.timedelta(today.weekday())
        this_week=this_week_uncut.replace(hour=0,minute=0,second=0,microsecond=0)

        self.set_is_week_in_period(this_week, week_delta)
        return week_delta

    def set_is_week_in_period(self, this_week, week_delta):
        """
        Sets week_bool whether the week is in the period the user wants or not (true or false)
        Called daily so filter is up to date

        :param this_week: the current week number
        :param week_delta: the timespan used for filtering
        """

        for week in self:
            year = week.year
            temp = datetime.datetime(year, 1, 1)
            temp = temp - datetime.timedelta(temp.weekday())
            delta = datetime.timedelta(days=(week.week_num - 1) * 7)
            start_date_of_week = temp + delta

            if week_delta >= 0:
                if this_week + datetime.timedelta(
                        weeks=week_delta) >= start_date_of_week and this_week <= start_date_of_week:
                    week.week_bool = True
                else:
                    week.week_bool = False

            else:
                if this_week + datetime.timedelta(
                        weeks=week_delta) <= start_date_of_week and this_week >= start_date_of_week:
                    week.week_bool = True
                else:
                    week.week_bool = False


    @api.depends('year', 'week_num')
    def build_week_string(self):
        """
        Builds and stores the week_string attribute
        based on year and week_num with a 'W' prefix, separated by a comma

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
    def check_if_week_num_is_valid(self):
        """
        Checks if week_num is within the valid range from 1 to 53

        :raises:
            :exception ValidationError: if week_num < 1 or week_num > 53
        """
        for r in self:
            if r.week_num < 1:
                raise exceptions.ValidationError("Week Number can't be smaller than 1")
            elif r.week_num > 53:
                raise exceptions.ValidationError("Week Number can't be bigger than 53")
