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

    @api.model_create_multi
    def add_weeks_object(self, week):
        weeks = self.env['week.model']
        return weeks.create(week)

    # Creating the "missing" week models for a project
    # TODO: Optimize week-representation (e.g. yyyy, W+weekNumber)
    # TODO: Optimize storing/loading the week model to/from the database so they can be displayed in chronological order
    @api.model
    def create(self, values):
        rec = super(Resource, self).create(values)
        week_data = rec.get_weeks(rec.start_date, rec.end_date, rec)

        for week in week_data:
            exists = self.env['week.model'].search([('week_num', '=', week['week_num'])])
            if not exists:
                rec.add_weeks_object(week)
        return rec

    def get_weeks(self, start_date, end_date, rec):
        start = self.env['leistung.model'].search([])
        if start:
            min_date = min(start.mapped('start_date'))
            max_date = max(start.mapped('end_date'))

            if rec.start_date < min_date:
                start_week = rec.start_date.isocalendar()[1]
            else:
                start_week = min_date.isocalendar()[1]

            if rec.end_date > max_date:
                end_week = rec.end_date.isocalendar()[1]
            else:
                end_week = max_date.isocalendar()[1]
        else:
            start_week = rec.start_date.isocalendar()[1]
            end_week = rec.end_date.isocalendar()[1]

        i = start_week
        week_data_array = []
        while i <= end_week:
            week_data = {}
            week_data['week_num'] = i
            week_data_array = week_data_array + [week_data]
            i = i + 1
        return week_data_array

    def get_first_week(self):
        start = datetime.date.min
