# -*- coding: utf-8 -*-
{
    'name': "Listado de Facturas por Organismos",

    'summary': """
        Se agrega la vista y el reporte de Listado de Facturas por Organismos""",

    'description': """
         Se agrega la vista y el reporte de Listado de Facturas por Organismos
    """,

    'author': "Interfaces S.A",
    'website': "http://www.interfaces.com.py",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Account',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','interfaces_timbrado'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/listado_facturas.xml',
        'views/wizard.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}