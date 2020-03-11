from odoo import models, fields
import datetime


class Resource(models.Model):
    _name = "resource.model"
    _rec_name = 'project'
    project = fields.Many2one('project.project', 'Project')
    employee = fields.Many2one('hr.employee', 'Employee')
    workload = fields.Integer(string='Arbeit', required=True)
    startDate = fields.Datetime(string='Start Datum')
    endDate = fields.Datetime(string='End Datum')


