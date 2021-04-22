# -*- coding: utf-8 -*-
{
    'name': "Ajustes MRP INTN - 2",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Interfaces S.A",
    'website': "http://www.interfaces.com.py",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'MRP',
    'version': '0.2020.1.20',

    # any module necessary for this one to work correctly
    'depends': ['base','mrp','sale_stock','campos_intn','account'],

    # always loaded
    'data': [
        'data/data.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/jerarquias.xml',
        'views/mrp.xml',
        'views/mrp_workorder.xml',
        'views/sale_order.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}