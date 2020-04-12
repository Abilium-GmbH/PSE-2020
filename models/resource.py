from odoo import models, fields, api, exceptions
import datetime


def get_week(date):
    """
    Returns the year and week of a given date as Int in
    the format YYYYWW  (Y Year, W Week)

    :param date:
    :return: year and week: YYYYWW
    """
    year = date.isocalendar()[0]
    week = date.isocalendar()[1]
    return year * 100 + week


class Resource(models.Model):
    """
    A class to assign employees a workload for a period of time in a project

    :param project: refers to an existing project from the project model, is required
    :param employee: refers to an existing employee from the employee model, is required
    :param workload: an integer representing the workload in percent (from 0 to 100), is required
    :param start_date: the date on which the assignment begins, is required
    :param end_date: the date on which the assignment end, is required
    start_date has to be before the end_date
    """
    _name = "resource.model"
    _rec_name = 'project'
    project = fields.Many2one('project.project', 'Project')
    employee = fields.Many2one('hr.employee', 'Employee')
    workload = fields.Integer(string='Workload', required=True)
    start_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string='End Date')

    @api.constrains('start_date', 'end_date')
    def check_start_date_before_end_date(self):
        """
        Checks if start date is before or at the same date as end date

        :raises:
            :exception ValidationError: if start_date > end_date
        :return: no return value
        """
        if self.start_date > self.end_date:
            raise exceptions.ValidationError("Start date must be before end date")

    @api.constrains('workload')
    def verify_workload(self):
        """
        Checks if workload is between 1 and 100

        :raises:
            :exception ValidationError: if workload <= 0 or workload > 100
        :return: no return value
        """
        if self.workload > 100:
            raise exceptions.ValidationError("The given workload can't larger than 100")
        elif self.workload <= 0:
            raise exceptions.ValidationError("The given workload can't be equal or smaller than 0")

    @api.model
    def create(self, values):
        """
        Constructor
        Initiates the creation of week.models, if missing
        Initiates the creation of corresponding weekly_resource.models

        :param values: requires a 'Project' which refers to an existing Project object,
            a 'Employee' which refers to an existing Employee object,
            a 'Workload' representing the workload in percent (from 0 to 100),
            a 'Start Date' on which the assignment begins
            and an 'End Date' on which the assignment ends
        :return: the created Resource object
        :rtype: resource
        """
        rec = super(Resource, self).create(values)
        rec.create_corresponding_models(rec)
        return rec

    def write(self, values):
        """
        Overriding default write method
        Delete old weekly_resource.models an creating new ones

        :param values,the values to be overwritten
        :return: rec
        :rtype: bool
        """
        rec = super(Resource, self).write(values)
        # Delete "old" weekly_resource.model
        old = self.env['weekly_resource.model'].search([['resource_id', '=', self.id]])
        if old:
            for model in old:
                model.unlink()

        # (Re-)Create "new" week.models or weekly_resource.models
        self.create_corresponding_models(self)
        return rec

    def create_corresponding_models(self, rec):
        """
        Creates corresponding week.models (if missing) and weekly_resource.models
        :param rec: the resource.model requiring the other models
        :return: None
        """
        # Create week.model
        week_data = rec.get_weeks(rec.start_date, rec.end_date)
        week_array = week_data[0]
        for week in week_array:
            exists = self.env['week.model'].search([['week_num', '=', week['week_num']], ['year', '=', week['year']]])
            if not exists:
                rec.add_weeks_object(week)

        # Create weekly_resource.model
        project_week_data = week_data[1]
        for week in project_week_data:
            week_model = self.env['week.model'].search(
                [['week_num', '=', week['week_num']], ['year', '=', week['year']]])
            values = {'week_id': week_model.id, 'resource_id': rec.id}
            rec.add_weekly_resource(values)
        return

    @api.model_create_multi
    def add_weeks_object(self, week):
        """
        Adds a week object to the weeks database

        :param week: the week which should be added to the database
        :return: the weeks with the newly added week
        """
        weeks = self.env['week.model']
        return weeks.create(week)

    @api.model_create_multi
    def add_weekly_resource(self, values):
        """
        Add an WeeklyResource object to the database

        :param values: requires a 'week_id' which refers to an existing Weeks object
            and a 'resource_id' which refers to an existing Resource object
        :return: the WeeklyResource
        """
        weekly_resource = self.env['weekly_resource.model']
        return weekly_resource.create(values)

    def get_weeks(self, start_date, end_date):
        """
        Computes the subsequent weeks between the earliest start_date and the latest end_date of all resources.
        Returns two arrays. The first containing all weeks and the second containing all weeks of
        the resource, starting on start_date and ending on end_date.

        :param start_date: the start_date of the resource
        :param end_date: the end_date of the resource
        :return: array of all weeks and array of project weeks
        """
        dates = self.get_first_and_last_date(start_date, end_date)

        # store dates as Integers to allow comparative operations
        last_week = get_week(dates['last_date'])
        start_week = get_week(start_date)
        end_week = get_week(end_date)

        date_i = dates['first_date']  # date iterator
        week_i = get_week(date_i)  # week iterator

        week_array = []
        project_week_array = []

        while week_i <= last_week:
            # create dict object
            week_data = {'week_num': date_i.isocalendar()[1], 'year': date_i.isocalendar()[0]}

            week_array = week_array + [week_data]

            # add week to project_week_array
            if start_week <= week_i <= end_week:
                project_week_array = project_week_array + [week_data]
                
            # add one week time difference to the date
            date_i = date_i + datetime.timedelta(weeks=1)
            week_i = get_week(date_i)

        return [week_array, project_week_array]

    def get_first_and_last_date(self, start_date, end_date):
        """
        Computes the first start_date and the last end_date of all resources
        including the parameters.

        :param start_date: the start_date of the resource
        :param end_date: the end_date of the resource
        :return: first_date and last_date of all resources
        """
        start = self.env['resource.model'].search([])
        if start:
            min_date = min(start.mapped('start_date'))
            max_date = max(start.mapped('end_date'))

            first_date = start_date if start_date < min_date else min_date
            last_date = end_date if end_date > max_date else max_date
        else:
            first_date = start_date
            last_date = end_date

        return {'first_date': first_date, 'last_date': last_date}
