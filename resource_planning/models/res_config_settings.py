from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    """
    Extends res.config.settings to store module-specific parameters from settings page.
    The variable filter_weeks is used to change the duration of the filter "custom timespan" in the Overview of
    weekly_resource models.
    """

    _inherit = 'res.config.settings'
    filter_weeks = fields.Integer(string="Weeks Filter", default=8)

    def set_values(self):
        """
        Stores the parameters in the ir.config_parameter model where they can be easily accessed.
        Calls the set_weekdelta_week and triggers the is_week_in_period method of week.model.

        :return: the created ResConfigSettings Object
        """
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('resource_planning.filter_weeks', self.filter_weeks)

        self.set_weekdelta_week()

        return res

    @api.model
    def get_values(self):
        """
        Fetches the parameters from the ir.config_parameter model and creates the ResConfigSettings model.

        :return: the ResConfigSettings Object
        """

        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        filter_weeks = ICPSudo.get_param('resource_planning.filter_weeks')
        res.update(
            filter_weeks=int(filter_weeks)
        )
        return res

    def set_weekdelta_week(self):
        """
        Triggers the is_week_in_period method of the week models to (re-)set the week_bool
        every time the filter_weeks (duration) was changed through the settings page.

        """

        weeks = self.env['week.model'].search([])

        for week in weeks:
            week.is_week_in_period()
