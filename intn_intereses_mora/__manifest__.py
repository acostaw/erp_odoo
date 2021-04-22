# -*- coding: utf-8 -*-
{
    'name': "intn_intereses_mora",

    'summary': """
        Cálculo de intereses por Mora para la INTN""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Interfaces S.A.",
    'website': "http://www.interfaces.com.py",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '0.2019.12.26',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management', 'account','grupo_account_payment'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/data.xml',
        'views/account_invoice.xml',
        'views/res_config_settings.xml',
        'views/wizard_pago.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
