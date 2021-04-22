# -*- coding: utf-8 -*-
{
    'name': "Presupuesto ONM",

    'summary': """
        Agrega vista para Presupuesto de ONM""",

    'description': """
        Agrega vista para Presupuesto de ONM
    """,

    'author': "Interfaces S.A",
    'website': "http://www.interfaces.com.py",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','campos_intn','presupuestos_intn','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/presupuesto_metrologia.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}