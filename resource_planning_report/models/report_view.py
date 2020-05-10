from datetime import datetime, timedelta

from odoo import models, fields, api


class ReportView(models.AbstractModel):
    """
        Abstract Model for report template.
    """
    _name = 'report.resource_planning_report.planning_report_view'

    @api.model
    def _get_report_values(self, docids, data=None):
        weeks = data['form']['weeks']
        length = len(weeks)
        docs = []

        projects = self.env['project.project'].search([])
        employees = self.env['hr.employee'].search([])

        for project in projects:
            for employee in employees:
                weekly_resource = self.env['weekly_resource.model'].search([
                    ['project', '=', project.id], ['employee', '=', employee.id]])

                # iterate through week-span
                week_array = []
                for i in range(length):
                    is_set = False
                    for res in weekly_resource:
                        if res.week_string == weeks[i]:

                            # check whether there already is an element with this week_string and delete it
                            for week_data in week_array:
                                if res.week_string == week_data['week']:
                                    week_array.remove(week_data)
                            week_array.append({'week': weeks[i],
                                               'workload': res.weekly_workload})
                            is_set = True
                        else:
                            if not is_set:
                                week_array.append({'week': weeks[i],
                                                   'workload': 0})
                                is_set = True

                if week_array:
                    print(employee.name)
                    print(str(week_array))
                    docs.append({'project': project.name,
                                 'employee': employee.name,
                                 'weekly_data': week_array
                                 })

        week_array = []
        for week in weeks:
            weekly_total = 0
            for doc in docs:
                for weekly_data in doc['weekly_data']:
                    if week == weekly_data['week']:
                        weekly_total = weekly_total + weekly_data['workload']
            week_array.append({'week': week,
                               'workload': weekly_total
                               })

        docs.append({'project': ' ',
                     'employee': 'Total',
                     'weekly_data': week_array
                     })
        print('Weeks')
        print(str(weeks))

        result = {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'weeks': weeks,
            'docs': docs,
        }

        print(str(result))

        return result