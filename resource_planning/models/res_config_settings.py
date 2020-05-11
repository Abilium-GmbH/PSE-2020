from odoo import fields, models, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    filter_weeks = fields.Integer(string="Weeks Filter", default=8)

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('resource_planning.filter_weeks', self.filter_weeks)

        self.set_weekdelta_week()


        return res


    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        filter_weeks = ICPSudo.get_param('resource_planning.filter_weeks')
        res.update(
            filter_weeks = int(filter_weeks)
        )
        return res


    def set_weekdelta_week(self):

        weeks = self.env['week.model'].search([])

        for week in weeks:
            week.is_week_in_period()


    