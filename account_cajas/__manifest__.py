# -*- coding: utf-8 -*-
{
    'name': "Cajas",

    'summary': """
       Agrega funcionalidad de cajas de pagos""",

    'description': """
        Agrega funcionalidad de cajas de pagos
    """,

    'author': "Interfaces S.A.",
    'website': "http://www.interfaces.com.py",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Account',
    'version': '2019.12.01',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account','grupo_account_payment'],

    # always loaded
    'data': [
        'data/data.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/cajas.xml',
        'views/caja_session.xml',
        'views/reporte_sesion_caja.xml',
        'views/reporte_sesion_caja_intn.xml',
        'views/account_journal.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
