# -*- coding: utf-8 -*-
{
    'name': "Multi Select Factura",

    'summary': """
        Módulo que agrega las funcionales para agregar más de un producto a la vez en las facturas""",

    'description': """
         Módulo que agrega las funcionales para agregar más de un producto a la vez en las facturas
    """,

    'author': "Interfaces S.A",
    'website': "http://www.interfaces.com.py",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Account',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/multi_product.xml',
        'views/account_invoice.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}