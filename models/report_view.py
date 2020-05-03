from datetime import datetime, timedelta

from odoo import models, fields, api


class ReportView(models.AbstractModel):
    """
        Abstract Model for report template.
    """
    _name = 'report.pse2020_resource_planning_report_view'

    @api.model
    def _get_report_values(self, docids, data=None):
        start_week = data['form']['start_week']
        end_week = data['form']['end_week']

        weekly_resources = self.env['weekly_resource.model']

        docs = []
        for res in weekly_resources:
            if res.year >= start_week.year & res.year >= end_week.year:
                if res.year > start_week.year | res.week_num >= start_week.week_num:
                    if res.year < end_week.year | res.week_num <= end_week.week_num:
                        docs.append({'week': res.week_string,
                                     'project': res.project.name,
                                     'employee': res.employee.name,
                                     'workload': res.weekly_workload})

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'start_week': start_week,
            'end_week': end_week,
            'docs': docs,
        }