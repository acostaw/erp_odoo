# -*- coding: utf-8 -*-
{
    'name': "Campos extras para la INTN",

    'summary': """
        En este modulo se agregan los campos extras para la INTN""",

    'description': """
        En este modulo se agregan los campos extras para la INTN
    """,

    'author': "Interfaces S.A. ",
    'website': "http://www.intefaces.com.py",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'INTN',
    'version': '0.2020.01.01',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'sale_management','contacts'],

    # always loaded
    'data': [
        'data/data.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/res_partner.xml',
        'views/product_template.xml',
        'views/jerarquias.xml',
        'views/contratos.xml',
        'views/resoluciones.xml',
        'views/resoluciones_viatico.xml',
        'views/res_expediente.xml',
        'views/intn_vehiculo.xml',
        'views/res_config_settings.xml',
        'views/res_country_state.xml',
        'views/account_invoice.xml',
        'views/mrp_workcenter.xml',
        'views/jerarquias.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
