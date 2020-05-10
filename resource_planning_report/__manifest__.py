# -*- coding: utf-8 -*-
{
    'name': "resource_planning_report",

    'summary': """
        Extends resource_planning by adding report-feature
    """,

    'description': """
        Provides PDF-Report for resouce_planning
    """,

    'author': "Cyrill Rohrbach, Gillian Cathomas, Sophie Pfister, Joel Hari, Jonas Ph. Kocher",
    'website': "https://github.com/Abilium-GmbH/PSE-2020",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'hr',
                'project',
                'resource_planning'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/report_wizard.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
