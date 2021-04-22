# -*- coding: utf-8 -*-
{
    'name': "Solicitudes de Servicio",

    'summary': """
        Modulo que agrega las solicitudes se servicio""",

    'description': """
        Modulo que agrega las solicitudes se servicio
    """,

    'author': "Interfaces S.A",
    'website': "http://www.interfaces.com.py",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale/Portal',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','portal','presupuestos_intn','sale_order_portal','campos_intn'],

    # always loaded
    'data': [
        'data/data.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/solicitudes_servicio.xml',
        'views/solicitudes_servicio_report.xml',
        'views/product_template.xml',
        'views/sale_portal_templates.xml',
        'views/templates.xml',
        'views/res_partner.xml',
        'views/intn_bascula.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}