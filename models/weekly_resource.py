
from odoo import models, fields, api


class WeeklyResource(models.Model):
    """
    A class that represents the mapping between a resource and a week.

    :param week_id: refers to an existing week from the week model
    :param resource_id: refers to an existing resource from the resource model
    """
    _name = "weekly_resource.model"
    _description = "Weekly Resource"
    _inherits = {'resource.model': 'resource_id',
                 'week.model': 'week_id'}

    week_id = fields.Many2one('week.model', 'Week Id', required=True, ondelete="cascade")
    resource_id = fields.Many2one('resource.model', 'Resource Id', required=True, ondelete="cascade")
    weekly_workload = fields.Integer(string='Workload %')
