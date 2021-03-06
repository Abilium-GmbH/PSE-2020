from odoo import models, fields, api, exceptions


class ReportWizard(models.TransientModel):
    """
    Interacts with the user to create the desired report.
    Asks the user for start_week and end_week, calculates the time span and passes it on.

    """
    _name = 'resource.planning.report.wizard'
    _description = 'Wizard to create Report'

    start_week = fields.Many2one('week.model', 'Start Week', required=True)
    end_week = fields.Many2one('week.model', 'End Week', required=True)

    def get_report(self):
        """
        Called when the user pushes the get-report button in the UI.
        Computes data and passes it on.

        """

        # Calculate time span
        weeks = self.get_weeks()

        # Define data
        data = {
            'model': self._name,
            'ids': self.ids,
            'form': {
                'weeks': weeks
            },
        }

        # Pass data to the report
        return self.env.ref('resource_planning_report.planning_report').report_action(self, data)

    @api.constrains('start_week', 'end_week')
    def start_week_before_end_week(self):
        """
        Checks, whether start_week is before end_week
        :raise
            :exception ValidationError
        """

        if self.end_week.year < self.start_week.year:
            raise exceptions.ValidationError("Start week must be before end week")
        elif self.start_week.year == self.end_week.year and self.start_week.week_num > self.end_week.week_num:
            raise exceptions.ValidationError("Start week must be before end week")

    def get_weeks(self):
        """
        Calculates timespan according to the user input for start_week and end_week
        :return: an array of week_string
        """
        start = self.start_week
        end = self.end_week
        weeks = []
        week_models = self.env['week.model'].search([])

        for week in week_models:
            if (week.week_string >= start.week_string) & (week.week_string <= end.week_string):
                weeks.append(week.week_string)

        weeks = self.order_weeks(weeks)
        return weeks

    def order_weeks(self, weeks):
        """
        Orders the week-strings chronologically for the report.

        :param weeks: the weeks defining the timespan for the report
        :return: the same week-string in chronological order
        """
        length = len(weeks)
        l = length
        result = []
        while len(result) != length:
            temp = weeks[0]
            index = 0
            for i in range(l):
                if weeks[i] < temp:
                    temp = weeks[i]
                    index = i
            result.append(temp)
            del(weeks[index])
            l = l-1

        return result
