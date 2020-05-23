from datetime import datetime, timedelta

from odoo import models, fields, api


class ReportView(models.AbstractModel):
    """
        Abstract Model for report template.
        Computes the required data for report.
    """
    _name = 'report.resource_planning_report.planning_report_view'  #
    _description = 'Computes values for report view'

    @api.model
    def _get_report_values(self, docids, data=None):
        """
        Computes the data for the report by going through all weekly_resource-models,
        trying to match them with the user-selected time span and gathering the relevant data.

        :param docids: the doc_id to be concatenated to the file name, passed on from report_wizard
        :param data: passed on from the report_wizard
        :return: the required data for report
        """
        weeks = data['form']['weeks']
        length = len(weeks)

        # result
        docs = []

        # Get a list  of all projects and employees
        projects = self.env['project.project'].search([])
        employees = self.env['hr.employee'].search([])

        # Iterate through projects and employees
        for project in projects:
            for employee in employees:
                weekly_resource = self.env['weekly_resource.model'].search([
                    ['project', '=', project.id], ['employee', '=', employee.id]])

                # iterate through week-span
                week_array = []
                for i in range(length):
                    is_set = False
                    # look for matching weekly_resources
                    for res in weekly_resource:
                        if res.week_string == weeks[i]:
                            # check whether there already is an element with this week_string and delete it
                            for week_data in week_array:
                                if res.week_string == week_data['week']:
                                    week_array.remove(week_data)
                            # add workload to to the resources week_array
                            week_array.append({'week': weeks[i],
                                               'workload': res.weekly_workload})
                            is_set = True
                        # else: set up resource with workload 0 and add it to the week_array
                        elif not is_set:
                            week_array.append({'week': weeks[i],
                                               'workload': 0})
                            is_set = True

                # add relevant data to docs
                if self.is_relevant(week_array):
                    docs.append({'project': project.name,
                                 'employee': employee.name,
                                 'weekly_data': week_array
                                 })

        # Calculate the total for each week
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
        # Add total to docs
        docs.append({'project': ' ',
                     'employee': 'Total',
                     'weekly_data': week_array
                     })

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'weeks': weeks,
            'docs': docs,
        }

    def is_relevant(self, week_array):
        """
        Checks whether the data in a week_array is relevant for the report
        (if there is a workload != 0)

        :return: boolean, indicating whether the data is relevant or not
        """
        for week in week_array:
            if week['workload'] != 0:
                return True

        return False
