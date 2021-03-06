from odoo import models, fields, api, exceptions
import datetime


def get_week(date):
    """
    Returns the year and week of a given date as Integer in
    the format YYYYWW  (Y Year, W Week)

    :param date:
    :return: year and week: YYYYWW
    """
    year = date.isocalendar()[0]
    week = date.isocalendar()[1]
    return year * 100 + week



class Resource(models.Model):
    """
    A class to assign employees a workload for a period of time in a project.

    """
    _name = "resource.model"
    _description = "Resource"
    _rec_name = 'project'

    project = fields.Many2one('project.project', 'Project', required=True)
    employee = fields.Many2one('hr.employee', 'Employee', required=True)
    base_workload = fields.Integer(string='Workload in %', required=True, help='Workload per week in percentage')
    start_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string='End Date')
    next_week = fields.Boolean(string='Next Week')
    weekly_resources = fields.One2many('weekly_resource.model', 'resource_id')
    weeks_to_be_added = fields.Integer(default=0, readonly="1",
                                       help='Weeks to be added or subtracted to/from current resource, changing the end date')

    @api.depends('weeks_to_be_added')
    def plus_one_week(self):
        """
        Sets end date one week later leaves start date as it was

        :returns date for end_date that will be set/updated
        """
        self.end_date = self.end_date + datetime.timedelta(days=7)
        self.weeks_to_be_added = self.weeks_to_be_added + 1

    @api.depends('weeks_to_be_added')
    def minus_one_week(self):
        """
        Sets end date one week earlier leaves start date as it was

        :returns date for end_date that will be set/updated
        """
        self.end_date = self.end_date - datetime.timedelta(days=7)
        self.weeks_to_be_added = self.weeks_to_be_added - 1

    @api.onchange('next_week')
    def set_dates(self):
        """
        Sets start and end date to coming monday and friday if next_week box is ticked

        :returns dates for start_date and end_date that will be set
        """
        if self.next_week:
            today = datetime.datetime.today()
            for day in range(1, 8):
                if today.isoweekday() != 1:
                    today = today + datetime.timedelta(days=1)
                elif today.isoweekday() == 1:
                    self.start_date = today
                    self.end_date = today + datetime.timedelta(days=4)

    @api.constrains('start_date', 'end_date')
    def verify_start_and_end_dates(self):
        """
        Checks if start date is before or at the same date as end date
        makes sure both dates are filled out

        :raises:
            :exception ValidationError: if start_date > end_date or one of the dates has not been entered (is False)
        """
        if self.start_date is False or self.end_date is False:
            raise exceptions.ValidationError("Both dates must be filled out")
        if self.start_date > self.end_date:
            raise exceptions.ValidationError("Start date must be before end date")

    @api.constrains('base_workload')
    def verify_workload(self):
        """
        Checks if workload is between 0 and 100

        :raises:
            :exception ValidationError: if workload < 0 or workload > 100
        """
        if self.base_workload > 100:
            raise exceptions.ValidationError("The given workload can't be larger than 100 %")
        elif self.base_workload < 0:
            raise exceptions.ValidationError("The given workload can't be smaller than 0 %")

    @api.model
    def create(self, values):
        """
        Constructor
        Initiates the creation corresponding models (of type Week, WeeklyResource)

        :param values: the user input to create a Resource object:
                        an employee and a project which are assigned to each other with a workload (base_workload),
                        start_date and end_date to define the timespan of the assignment,
                        as well as some other used for some computations on the object

        :return: the created Resource object
        """
        rec = super(Resource, self).create(values)
        rec.create_corresponding_models(rec)
        return rec

    def write(self, values):
        """
        Overriding default write method (modifying a Resource model)
        Calls create_corresponding_models method to delete spare and create new weekly_resources.

        :param values: the "new" values to be stored in the database
        :param self: the Resource model to be modified
        :return: rec: a boolean indicating whether write has been successful or not
        :rtype: bool
        """
        rec = super(Resource, self).write(values)

        self.create_corresponding_models(self)

        return rec

    def create_corresponding_models(self, rec):
        """
        Creates corresponding week.models (if missing).
        Creates corresponding weekly_resource.models (if missing) and
        deletes weekly_resource.models which are not within the start_date
        and end_date anymore (when updating a resource model).

        :param rec: the Resource model which requires the other models
        """
        # Create missing week.model
        week_data = rec.compute_weeks(rec.start_date, rec.end_date)
        week_array = week_data[0]
        for week in week_array:
            exists = self.env['week.model'].search([['week_num', '=', week['week_num']], ['year', '=', week['year']]])
            if not exists:
                rec.add_weeks_object(week)

        # Create weekly_resource.model
        project_week_data = week_data[1]
        rec.add_missing_weekly_resources(project_week_data)
        rec.delete_spare_weekly_resources(project_week_data)

    def add_missing_weekly_resources(self, project_week_data):
        """
        Creates a new weekly_resource for all weeks in project_week_date
        if it does not exist yet

        :param project_week_data: all weeks (defining the timespan) of the resource
        """
        for week in project_week_data:
            exists = self.env['weekly_resource.model'].search([['resource_id', '=', self.id],
                                                               ['week_id.week_num', '=', week['week_num']],
                                                               ['week_id.year', '=', week['year']]])

            if exists and not(exists.manually_changed):
                exists.weekly_workload = self.base_workload

            if not exists:
                week_model = self.env['week.model'].search([['week_num', '=', week['week_num']],
                                                        ['year', '=', week['year']]])

                if self.employee.compute_total_workload(week_model) + self.base_workload > 100:
                    raise exceptions.ValidationError("The workload in week " + week_model.week_string + " is too high")

                values = {'week_id': week_model.id, 'resource_id': self.id, 'weekly_workload': self.base_workload}
                self.add_weekly_resource(values)


    def delete_spare_weekly_resources(self, project_week_data):
        """
        Deletes all corresponding weekly_resources to this resource
        if the week is not in the project_week_array (anymore).

        :param project_week_data: all weeks (defining the timespan) of the resource
        """
        weekly_resources = self.env['weekly_resource.model'].search([['resource_id', '=', self.id]])
        for weekly_resource in weekly_resources:
            exists = False
            for week in project_week_data:
                if week['week_num'] == weekly_resource.week_id.week_num and \
                        week['year'] == weekly_resource.week_id.year:
                    exists = True

            if not exists:
                weekly_resource.unlink()

    @api.model_create_multi
    def add_weeks_object(self, week):
        """
        Adds a week object to the database (table weeks.model)

        :param week: the week to be added to the database
        :return: the newly created week
        """
        weeks = self.env['week.model']
        return weeks.create(week)

    @api.model_create_multi
    def add_weekly_resource(self, values):
        """
        Add an WeeklyResource model to the database (table weekly_resource.model)

        :param values: the required values to create a WeeklyResource model:
                week_id and resource_id to link to corresponding models,
                weekly_workload to declare the workload an employee is working on a project in this week
        :return: the created WeeklyResource
        """
        weekly_resource = self.env['weekly_resource.model']
        return weekly_resource.create(values)

    def compute_weeks(self, start_date, end_date):
        """
        Computes the subsequent weeks between the earliest start_date and the latest end_date of all resources.
        Computes also all weeks in the timespan of a Resource model.
        Returns both as arrays.
        Called when a Resource model is created or modified.

        :param start_date: the start_date of the Resource
        :param end_date: the end_date of the Resource
        :return: 2 arrays of week-data, one covering the timespan of all Resources, the other one only of the Resource

        """
        dates = self.compute_first_and_last_date(start_date, end_date)

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

    def compute_first_and_last_date(self, start_date, end_date):
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
