# -*- coding: utf-8 -*-
{
    'name': "Grupos de pagos",

    'summary': """
        Grupos de pagos
        """,

    'description': """
        Añade la funcionalidad de agrupar diferentes métodos de pago en un solo recibo u orden de pago
    """,

    'author': "Interfaces S.A.",
    'website': "http://www.interfaces.com.py",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Account',
    'version': '0.2020.01.01',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'data/data.xml',
        'views/templates.xml',
        'views/payment_group.xml',
        'views/account_payment.xml',
        'views/account_invoice.xml',
        'views/reporte_pagos.xml',
        'views/journal_dashboard.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'post_init_hook': 'post_init_hook'
}
