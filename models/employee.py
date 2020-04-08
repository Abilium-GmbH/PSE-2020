from odoo import models, fields


class Employee(models.Model):
    """
    Inherits the 'employee' model from the 'hr' App
    """
    _inherit = 'hr.employee'
    # total_workload_planed = fields.Integer(compute='_calculate_planed', string="Total", store=True)

    # TODO: Improve this to check the weekly workload (Iteration 3)
    # def _calculate_planed(self):
    #     for employee in self:
    #         query = self.env['resource.model'].search([('employee', '=', employee.id)])
    #         total = sum(query.mapped('workload'))
    #         employee.total_workload_planed = total
    #     return 0
