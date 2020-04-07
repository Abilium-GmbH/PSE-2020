
from odoo import models, fields, api, exceptions
import datetime


# returns the year and week of a given datetime
# format: YYYYWW   (Y - Year, W - Week)
def get_week(date):
    year = date.isocalendar()[0]
    week = date.isocalendar()[1]
    return year * 100 + week


class Resource(models.Model):
    _name = "resource.model"
    _rec_name = 'project'
    project = fields.Many2one('project.project', 'Project')
    employee = fields.Many2one('hr.employee', 'Employee')
    workload = fields.Integer(string='Workload', required=True)
    start_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string='End Date')

    # checks that start date is before or at the same date as end date
    @api.constrains('start_date', 'end_date')
    def check_start_date_before_end_date(self):
        if self.start_date > self.end_date:
            raise exceptions.ValidationError("Start date must be before end date")

    # checks if: 0 < workload <= 100
    @api.constrains('workload')
    def verify_workload(self):
        if self.workload > 100:
            raise exceptions.ValidationError("The given workload can't larger than 100")
        elif self.workload <= 0:
            raise exceptions.ValidationError("The given workload can't be equal or smaller than 0")

    # Constructor
    # Initiates the creation of missing week.models
    # Initiates the creation of corresponding weekly_resource.models
    @api.model
    def create(self, values):
        # Create resource.model
        rec = super(Resource, self).create(values)

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
    def get_weeks(self, start_date, end_date):
        start = self.env['resource.model'].search([])
        if start:
            min_date = min(start.mapped('start_date'))
            max_date = max(start.mapped('end_date'))

            first_date = start_date if start_date < min_date else min_date

            last_date = end_date if end_date > max_date else max_date
        else:
            first_date = start_date
            last_date = end_date

        # store dates as Integers to allow comparative operations
        last_week = get_week(last_date)
        start_week = get_week(start_date)
        end_week = get_week(end_date)

        date_i = first_date  # date iterator
        week_i = get_week(date_i)  # week iterator

        week_array = []
        project_week_array = []

        while week_i <= last_week:
            # create dict object
            week_data = {'week_num': date_i.isocalendar()[1], 'year': date_i.isocalendar()[0]}

            # add object to array that can be returned
            week_array = week_array + [week_data]

            # add week to project_week_array
            if start_week <= week_i <= end_week:
                project_week_array = project_week_array + [week_data]

            # add one week time difference to the date
            date_i = date_i + datetime.timedelta(weeks=1)
            week_i = get_week(date_i)

        return [week_array, project_week_array]
