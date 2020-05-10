from odoo import models, fields


class Project(models.Model):
    """
    Inherits the 'project' model from the 'project' App
    """
    _inherit = 'project.project'
    # total_planed_workload = fields.Integer(compute='calculate_planed_workload', string="Planned Workload", store=True)

    # def calculate_planed_workload(self):
    #     for project in self:
    #         query = self.env['resource.model'].search([('project','=',project.id)])
    #         total = sum(query.mapped('workload'))
    #         project.total_planed_workload = total
    #     return 0
