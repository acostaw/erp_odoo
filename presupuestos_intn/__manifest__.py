# -*- coding: utf-8 -*-
{
    'name': "Expediente INTN",

    'summary': """
        Expediente INTN
        """,

    'description': """
        Expediente INTN
    """,

    'author': "Interfaces S.A.",
    'website': "http://www.interfaces.com.py",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Invoicing',
    'version': '0.2020.01.02',

    # any module necessary for this one to work correctly
        'depends': ['base','account', 'l10n_py','campos_intn'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/data.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/expediente.xml',
        'views/sale_order.xml',
        'views/res_config_settings.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
