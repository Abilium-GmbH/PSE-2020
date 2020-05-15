from odoo import models, fields


class Project(models.Model):
    """
    Inherits the 'project' model from the 'project' app.
    Might be extended to provide more functionality required by resource_planning module.
    """
    _inherit = 'project.project'

