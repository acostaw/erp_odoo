# -*- coding: utf-8 -*-
{
    'name': "Listado Servicios Facturados por Departamentos de Pais",

    'summary': """
        Listado Servicios Facturados por Departamentos de Pais""",

    'description': """
        Listado Servicios Facturados por Departamentos de Pais
    """,

    'author': "Interfaces S.A.",
    'website': "http://www.interfaces.com.py",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Account',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','intn_intereses_mora','interfaces_facturas'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/servicios_departamentos.xml',
        'views/intn_organismos.xml',
        'views/wizard.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}