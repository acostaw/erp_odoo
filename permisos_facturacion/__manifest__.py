# -*- coding: utf-8 -*-
{
    'name': "Permisos de facturacion",

    'summary': """
        Modifica los permisos por defecto de la facturación
        """,

    'description': """
        El permiso 'Facturacion' se cambia a 'Facturacion (solo lectura)'
        Se agrega un permiso nuevo 'Facturacion' que permite crear facturas
    """,

    'author': "Interfaces S.A.",
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
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'data/data.xml',
        'views/account_invoice.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}