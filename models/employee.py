from odoo import models, fields


class Employee(models.Model):
    """
    Inherits the 'employee' model from the 'hr' App
    """
    _inherit = 'hr.employee'

    resources = fields.One2many('resource.model', 'employee')

    def get_total_workload(self, week):
        """
        Computes the total workload assigned to the employee in a specific week

        :param week: week model of the desired week
        :return: total workload in that week
        """
        total_workload = 0

        for resource in self.resources:
            for weekly_resource in resource.weekly_resources:
                if weekly_resource.week_id == week:
                    total_workload += weekly_resource.weekly_workload

        return total_workload
