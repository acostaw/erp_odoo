# -*- coding: utf-8 -*-
{
    'name': "Uso de Marca",

    'summary': """
        En este módulo se agregan las especificaciones para el presupuesto de Uso de Marca""",

    'description': """
        En este módulo se agregan las especificaciones para el presupuesto de Uso de Marca
    """,

    'author': "Interfaces S.A",
    'website': "http://www.interfaces.com.py",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','campos_intn', 'presupuestos_intn'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/sale_order.xml',
        'views/etapas.xml',
        'views/uso_marca_conformidad.xml',
        'views/uso_marca_sistema.xml',
        'views/uso_marca_interno.xml',
        'views/sub_etapas.xml',
        'views/metodos_pago.xml',
        'views/product_template.xml',
        'data/data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}