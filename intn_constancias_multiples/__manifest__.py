# -*- coding: utf-8 -*-
{
    'name': "Constancias múltiples INTN",

    'summary': """
        Modulo que agrega la generacion de constancias múltiples""",

    'description': """
         Modulo que agrega la generacion de constancias múltiples
    """,

    'author': "Interfaces S.A.",
    'website': "http://www.interfaces.com.py",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'MRP',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale','campos_intn','mrp','intn_constancias','portal'],

    'qweb':[
        'static/src/xml/button_crear.xml',
        'static/src/xml/widget.xml',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/constancias_multiples.xml',
        'views/constancia_portal_template.xml',
        'views/plantilla_constancias.xml',
        'views/tipo_constancia.xml',
        'views/wizard.xml',
        'views/constancia.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}