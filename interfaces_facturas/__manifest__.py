# -*- coding: utf-8 -*-
{
    'name': "Facturas Interfaces",

    'summary': """
        Facturas Interfaces
        """,

    'description': """
        Facturas Interfaces
    """,

    'author': "Interfaces S.A.",
    'website': "http://www.interfaces.com.py",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Invoicing',
    'version': '0.2020.01.01',

    # any module necessary for this one to work correctly
    'depends': ['base','account', 'l10n_py'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/data.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/factura.xml',
        'views/credito.xml',
        'views/account_invoice.xml',
        'views/account_journal.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}