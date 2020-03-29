# -*- coding: utf-8 -*-
{
    'name': "Resource Planning",

    'summary': """
        This module can be used to allocate human resources to projects""",

    'description': """
        tbd
    """,

    'author': "Cyrill Rohrbach, Gillian Cathomas, Sophie Pfister, Joel Hari, Jonas Kocher",
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
        'views/projects.xml',
        'views/employees.xml',
        'views/weeks.xml',
        'views/weekly_resource.xml'
    ],
    # only loaded in demonstration mode
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
