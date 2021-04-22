# -*- coding: utf-8 -*-
{
    'name': "Multi Select Presupuesto",

    'summary': """
        Módulo que agrega las funcionales para agregar más de un producto a la vez en los presupuestos""",

    'description': """
         Módulo que agrega las funcionales para agregar más de un producto a la vez en los presupuestos
    """,

    'author': "Interfaces S.A",
    'website': "http://www.interfaces.com.py",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management', 'product','presupuestos_intn'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/multi_product.xml',
        'views/sale_order.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
