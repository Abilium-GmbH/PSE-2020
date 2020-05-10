from odoo import models, fields, api, exceptions


class ReportWizard(models.TransientModel):
    """
    Interacts with the user to create the desired report.

    :param start_week, end_week: defining the timespan to be reported

    """
    _name = 'resource.planning.report.wizard'

    # TODO: week_string soll im Form angezeigt werden
    # TODO: evtl. weitere Filterkriterien?
    start_week = fields.Many2one('week.model', 'Start Week', required=True)
    end_week = fields.Many2one('week.model', 'End Week', required=True)


    def get_report(self):

        weeks = self.get_weeks()

        data = {
            'model': self._name,
            'ids': self.ids,
            'form': {
                'weeks': weeks
            },
        }

        return self.env.ref('resource_planning.resource_planning_report').report_action(self, data)

    @api.constrains
    def start_week_before_end_week(self):
        """
        Checks, whether start_week is before end_week
        :raise
            :exception ValidationError
        """

        if self.end_week.year < self.start_week.year:
            raise exceptions.ValidationError("Start week must be before end week")
        elif self.start_week.year == self.end_week.year & self.start_week.week_num > self.end_week.week_num:
            raise exceptions.ValidationError("Start week must be before end week")

    def get_weeks(self):
        start = self._get_week(self.start_week)
        end = self._get_week(self.end_week)
        weeks = []
        week_models = self.env['week.model'].search([])

        for week in week_models:
            if week.year < start.year | week.year > end.year:
                continue
            if week.year == start.year:
                if week.week_num < start.week_num:
                    continue
            if week.year == end.year:
                if week.week_num > end.week_num:
                    continue
            weeks.append(week.week_string)
        return weeks


    def _get_week(self, week):
        week_split = str(week).split('(')[1]
        week_id = int(week_split.split(',')[0])
        return self.env['week.model'].search([['id', '=', week_id]])




