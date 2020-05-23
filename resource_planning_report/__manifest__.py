# -*- coding: utf-8 -*-
{
    'name': "resource_planning_report",

    'summary': """
        Report feature for resource_planning module
    """,

    'description': """
        This module extends resource_planning module by adding the report function.
        The assigned resources during a user-selected time can be exported in PDF-Format.
        The resources are displayed in a clear table similar to the overview in resource_planning module.
        The total workload per week is calculated and displayed at the bottom of the table.
    """,

    'author': "Cyrill Rohrbach, Gillian Cathomas, Sophie Pfister, Joel Hari, Jonas Ph. Kocher",
    'website': "https://github.com/Abilium-GmbH/PSE-2020",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Administration',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'hr',
                'project',
                'resource_planning'],

    # always loaded
    'data': [
        'views/report_wizard.xml'
    ],
    # only loaded in demonstration mode
    'demo': [],
}
