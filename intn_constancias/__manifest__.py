# -*- coding: utf-8 -*-
{
    'name': "Constancias INTN",

    'summary': """
        Modulo que agrega la generacion de constancias""",

    'description': """
         Modulo que agrega la generacion de constancias
    """,

    'author': "Interfaces S.A.",
    'website': "http://www.interfaces.com.py",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'MRP',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale','campos_intn','mrp'],

    # always loaded
    'data': [
        'data/data.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/intn_constancia.xml',
        'views/product_template.xml',
        'views/constancia_report.xml',
        'views/online_constancia.xml',
        'views/email_template.xml',
        
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}