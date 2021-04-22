# -*- coding: utf-8 -*-

{
    'name': 'Paraguay - Contabilidad',
    'version': '0.1',
    'description': """
        Cuentas contables según Secretaría de Estado de Tributación.
        Impuestos.
    """,
    'author': ['Interfaces S.A.'],
    'category': 'Localization',
    'depends': ['base', 'account','grupos_cuentas'],
    'data':[
        'data/l10n_py_chart_data.xml',
        'data/account.group.csv',
        'data/account.account.template.csv',
        'data/l10n_py_chart_post_data.xml',
        'data/account_data.xml',
        'data/account_tax_data.xml',
        'data/account_chart_template_data.xml',
    ],
}
