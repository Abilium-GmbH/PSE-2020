
from odoo import models, fields, api, exceptions
from . import weeks
import datetime


class Resource(models.Model):
    _name = "resource.model"
    _rec_name = 'project'
    project = fields.Many2one('project.project', 'Project')
    employee = fields.Many2one('hr.employee', 'Employee')
    workload = fields.Integer(string='Workload', required=True)
    start_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string='End Date')

    #checks that start date is before or at the same date as enddate
    @api.constrains('start_date', 'end_date')
    def check_start_date_before_end_date(self):
        if self.start_date > self.end_date:
            raise exceptions.ValidationError("Start date must be before end date")

    # Constructor
    # Initiates the creation of missing week.models
    # Initiates the creation of corresponding weekly_resource.models
    @api.model
    def create(self, values):
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
            week_model = self.env['week.model'].search([['week_num', '=', week['week_num']], ['year', '=', week['year']]])
            values = {'week_id': week_model.id, 'resource_id': rec.id}
            rec.add_weekly_resource(values)
        return rec

    @api.model_create_multi
    def add_weeks_object(self, week):
        weeks = self.env['week.model']
        return weeks.create(week)

    @api.model_create_multi
    def add_weekly_resource(self, values):
        weekly_resource = self.env['weekly_resource.model']
        return weekly_resource.create(values)

    # Computes and returns weeks between the earliest start_date
    # and the latest end_date of all resources
    def get_weeks(self, start_date, end_date, rec):
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

    # Computes the weeks a resource takes place in
    def get_project_weeks(self, start_date, end_date, rec):
        start_week = rec.start_date.isocalendar()[1]
        start_year = rec.start_date.isocalendar()[0]
        end_week = rec.end_date.isocalendar()[1]
        end_year = rec.end_date.isocalendar()[0]
        week_data_array = rec.get_week_data(start_week, start_year, end_week, end_year)
        return week_data_array

    # Computes and returns all weeks between start_week and end_week
    def get_week_data(self, start_week, start_year, end_week, end_year):
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

    # Alert when trying to assign a workload of more than 100%
    @api.onchange('workload')
    def verify_workload(self):
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
    _name = "weekly_resource.model"
    _inherits = {'resource.model': 'resource_id',
                 'week.model': 'week_id'}

    week_id = fields.Many2one('week.model', 'Week Id', ondelete="cascade")
    resource_id = fields.Many2one('resource.model', 'Resource Id', ondelete="cascade")
