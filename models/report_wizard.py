from odoo import models, fields, api, exceptions


class ReportWizard(models.TransientModel):
    """
    Interacts with the user to create the desired report.

    :param start_week, end_week: defining the timespan to be reported

    """
    _name = 'resource_planning.report.wizard'

    start_week = fields.Many2one('week.model', 'Start Week', required=True)
    end_week = fields.Many2one('week.model', 'End Week', required=True)
    weeks = fields.Many2many('week.model', compute='get_weeks')


    def get_report(self):
        data = {
            'model': self._name,
            'ids': self.ids,
            'form': {
                'start_week': self.start_week, 'end_week': self.end_week,
            },
        }

        return self.env.ref('pse2020_resource_planning_report').report_action(self, data)

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

    @api.depends('start_week', 'end_week')
    def get_weeks(self):
        start = self.start_week
        end = self.end_week
        current = start
        weeks = []

        while current != end:
            weeks.append(current)

            temp = self.env['weeks.model'].search(
                    [['year', '=', current.year],
                    ['week_num', '=', (current.week_num + 1)]])
            if temp:
                current = temp
                continue
            else:
                year = current.year + 1;
                temp = self.env['weeks.model'].search(
                        [['year', '=', year],
                        ['week_num', '=', 1]])
                current = temp
                continue




