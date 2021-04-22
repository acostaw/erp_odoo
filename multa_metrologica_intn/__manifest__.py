# -*- coding: utf-8 -*-
{
    'name': "Multa Metrologica INTN",

    'summary': """
        Se agrega la vista y las funciones para la carga de  multas metrologicas por resolucion""",

    'description': """
        Se agrega la vista y las funciones para la carga de  multas metrologicas por resolucion
    """,

    'author': "Interfaces S.A.",
    'website': "http://www.interfaces.com.py",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','account','account_cajas'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/multa_metrologica.xml',
        'views/account_journal.xml',
        'views/wizard_factura.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}