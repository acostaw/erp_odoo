# -*- coding: utf-8 -*-
{
    'name': "Cuentas a cobrar y pagar - Community Edition",

    'summary': """
       Cuentas a cobrar y pagar - Community Edition""",

    'description': """
        Agrega vista de cuentas a cobrar y a pagar para la versión Community
    """,

    'author': "Interfaces S.A.",
    'website': "http://www.interfaces.com.py",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Account',
    'version': '2019.12.12',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/cuentas_cobrar.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}