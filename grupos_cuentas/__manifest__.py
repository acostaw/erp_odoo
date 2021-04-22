# -*- coding: utf-8 -*-
{
    'name': "Grupos de cuentas",

    'summary': """
        Agrega la funcionalidad de agrupar las cuentas contables
        """,

    'description': """
        Permite la gestión de Grupos de cuentas
        Agrega el codigo del grupo al nombre de la cuenta
        Cambia la validación de codigos duplicados permitiendo que dos cuentas puedan tener un mismo
        codigo si están en grupos distintos
    """,

    'author': "Interfaces S.A.",
    'website': "http://www.interfaces.com.py",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/account_group.xml',
    
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
