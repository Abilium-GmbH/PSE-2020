
from odoo import models, fields, api, exceptions


class WeeklyResource(models.Model):
    """
    A class that represents the mapping between a resource and a week.

    :param week_id: refers to an existing week from the week model
    :param resource_id: refers to an existing resource from the resource model
    """
    _name = "weekly_resource.model"
    _inherits = {'resource.model': 'resource_id',
                 'week.model': 'week_id'}

    week_id = fields.Many2one('week.model', 'Week Id', ondelete="cascade")
    resource_id = fields.Many2one('resource.model', 'Resource Id', ondelete="cascade")
    weekly_workload = fields.Integer(string='Workload in %')

    @api.constrains('weekly_workload')
    def verify_workload(self):
        """
        Checks if workload is between 1 and 100

        :raises:
            :exception ValidationError: if workload < 0 or workload > 100
        :return: no return value
        """
        if self.weekly_workload > 100:
            raise exceptions.ValidationError("The given workload can't be larger than 100")
        elif self.base_workload < 0:
            raise exceptions.ValidationError("The given workload can't be smaller than 0")
