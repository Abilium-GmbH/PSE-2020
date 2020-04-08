from odoo import models, fields, api, exceptions
from . import weeks
import datetime


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
        checks if start date is before or at the same date as end date
        :raises:
            :exception ValidationError: if start_date > end_date
        :return: no return value
        """
        if self.start_date > self.end_date:
            raise exceptions.ValidationError("Start date must be before end date")

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

        # Create resource.model
        rec = super(Resource, self).create(values)

        # Create week.model
        week_data = rec.get_weeks(rec.start_date, rec.end_date, rec)
        for week in week_data:
            exists = self.env['week.model'].search([['week_num', '=', week['week_num']], ['year', '=', week['year']]])
            if not exists:
                rec.add_weeks_object(week)

        # Create weekly_resource.model
        project_week_data = rec.get_project_weeks(rec.start_date, rec.end_date, rec)
        for week in project_week_data:
            week_model = self.env['week.model'].search(
                [['week_num', '=', week['week_num']], ['year', '=', week['year']]])
            values = {'week_id': week_model.id, 'resource_id': rec.id}
            rec.add_weekly_resource(values)
        return rec

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

    def get_weeks(self, rec):
        """
        Computes and returns the subsequent weeks
        between the earliest start_date and the latest end_date of all resource
        :param rec: the resource
        :return: array of weeks
        """
        start = self.env['resource.model'].search([])
        if start:
            min_date = min(start.mapped('start_date'))
            max_date = max(start.mapped('end_date'))

            if rec.start_date < min_date:
                start_week = rec.start_date.isocalendar()[1]
                start_year = rec.start_date.isocalendar()[0]
            else:
                start_week = min_date.isocalendar()[1]
                start_year = min_date.isocalendar()[0]

            if rec.end_date > max_date:
                end_week = rec.end_date.isocalendar()[1]
                end_year = rec.end_date.isocalendar()[0]
            else:
                end_week = max_date.isocalendar()[1]
                end_year = max_date.isocalendar()[0]
        else:
            start_week = rec.start_date.isocalendar()[1]
            start_year = rec.start_date.isocalendar()[0]
            end_week = rec.end_date.isocalendar()[1]
            end_year = rec.end_date.isocalendar()[0]

        week_data_array = rec.get_week_data(start_week, start_year, end_week, end_year)
        return week_data_array

    def get_project_weeks(self, rec):
        """
        Computes and returns the subsequent weeks a resource takes place in
        :param rec: the resource
        :return: array of weeks
        """
        start_week = rec.start_date.isocalendar()[1]
        start_year = rec.start_date.isocalendar()[0]
        end_week = rec.end_date.isocalendar()[1]
        end_year = rec.end_date.isocalendar()[0]
        week_data_array = rec.get_week_data(start_week, start_year, end_week, end_year)
        return week_data_array

    def get_week_data(self, start_week, start_year, end_week, end_year):
        """
        Computes and returns an array of subsequent weeks
        beginning from the start_week/start_year up to the end_week/end_year
        :param start_week: the week number where the array should start
        :param start_year: the year of the start_week
        :param end_week: the week number where the array should end
        :param end_year: the year of the end_week
        :return: array of weeks
        """
        if start_week == 0:
            start_week = 1
        if end_week == 0:
            end_week = 52
        j = start_year
        i = start_week
        week_data_array = []
        while j <= end_year:
            if j == end_year:
                end_week_j = end_week
            else:
                end_week_j = datetime.date(j, 12, 31).isocalendar()[1]
            while i <= end_week_j:
                week_data = {}
                week_data['week_num'] = i
                week_data['year'] = j
                week_data_array = week_data_array + [week_data]
                i = i + 1
            j = j + 1
            i = 1
        return week_data_array

    @api.onchange('workload')
    def verify_workload(self):
        """
        Alerts the user when trying to assign a workload outside the expected range
        :return: a warning if the workload is either larger than 100 or smaller than 0 (percent)
        """
        if self.workload > 100:
            return {'warning': {
                'title': "Workload too high",
                'message': "The given workload is too high for an employee",
            }, }
        elif self.workload <= 0:
            return {'warning': {
                'title': "Workload too low",
                'message': "The given workload can't be 0 or less",
            }, }


class WeeklyResource(models.Model):
    """
    A class that represents the mapping between a resource and a week.
    :param week_id: refers to an existing week from the week model
    :param resource_id: refers to an existing resource from the resource model
    """
    _name = "weekly_resource.model"
    _inherits = {'resource.model': 'resource_id',
                 'week.model': 'week_id'}

    week_id = fields.Many2one('week.model', 'Week Id', ondelete="cascade")
    resource_id = fields.Many2one('resource.model', 'Resource Id', ondelete="cascade")
