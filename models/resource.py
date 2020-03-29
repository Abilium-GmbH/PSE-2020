from odoo import models, fields, api
import datetime


class Resource(models.Model):
    _name = "resource.model"
    _rec_name = 'project'
    project = fields.Many2one('project.project', 'Project')
    employee = fields.Many2one('hr.employee', 'Employee')
    workload = fields.Integer(string='Workload', required=True)
    start_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string='End Date')

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
            exists = self.env['week.model'].search([['week_num', '=', week['week_num']],['year', '=', week['year']]])
            if not exists:
                rec.add_weeks_object(week)

        # Create weekly_resource.model
        # TODO: Determine data to be passed on to weekly_resource.model --> week-model?
        project_week_data = rec.get_project_weeks(rec.start_date, rec.end_date, rec)
        for week in project_week_data:
            week_num = week['week_num']
            values = {'week': week_num, 'resource_id': rec.id}
            rec.add_weekly_resource(values)

        return rec

    @api.onchange('workload')
    def verify_workload(self):
        if self.workload > 100:
            return {'warning': {
                'title': "Workload too high",
                'message': "The given workload is too high for an employee",
            }, }

    @api.model_create_multi
    def add_weeks_object(self, week):
        weeks = self.env['week.model']
        return weeks.create(week)

    @api.model_create_multi
    def add_weekly_resource(self, values):
        weekly_resource = self.env['weekly_resource.model']
        return weekly_resource.create(values)


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

        # TODO: Refactor to avoid duplicate code
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

    def get_project_weeks(self, start_date, end_date, rec):
        start_week = rec.start_date.isocalendar()[1]
        start_year = rec.start_date.isocalendar()[0]
        end_week = rec.end_date.isocalendar()[1]
        end_year = rec.end_date.isocalendar()[0]

        # TODO: Refactor to avoid duplicate code
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


class WeeklyResource(models.Model):
    _name = "weekly_resource.model"
    _inherits = {'resource.model': 'resource_id'}
    # TODO: Inherits also week.model?
    week = fields.Integer(string='Week')
    resource_id = fields.Many2one('resource.model', 'Resource Id', ondelete="cascade")

