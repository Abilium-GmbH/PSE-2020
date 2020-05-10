# -*- coding: utf-8 -*-
#

{
    'name': "resource_planning",

    'summary': """
        This module can be used to allocate human resources to projects""",

    'description': """
        With this module you can assign your employees from the HR app with your projects from the Project app.
        You can set their workload and look at it in the weekly overview. 
    """,

    'author': "Cyrill Rohrbach, Gillian Cathomas, Sophie Pfister, Joel Hari, Jonas Ph. Kocher",
    'website': "https://github.com/Abilium-GmbH/PSE-2020",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'project',
        'hr',
        ],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/resource_tree.xml',
        'views/weekly_resource.xml',
        'views/weekly_resource_project.xml',
        # 'report/report_wizard.xml'
    ],
    # only loaded in demonstration mode
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
