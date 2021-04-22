# -*- coding: utf-8 -*-
{
    'name': "Informe Bascula",

    'summary': """
        Módulo que agrega el informe de verificación de IPNA - Bascula""",

    'description': """
        Módulo que agrega el informe de verificación de IPNA - Bascula
    """,

    'author': "Interfaces",
    'website': "http://www.interfaces.com.py",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Account',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','portal','campos_intn','solicitudes_servicio','intn_constancias','account',],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/views.xml',
        'views/informes_bascula.xml',
        'views/online_informe_bascula.xml',
        'views/informe_bascula_report.xml',
        'views/informe_portal_template.xml',
        'views/intn_bascula.xml',
        'views/templates.xml',
        'views/email_template.xml',
        #'views/res_partner.xml',
        'views/wizard.xml',
        'views/listado_informe_bascula.xml',
        'views/calcomanias_informe.xml',
        'views/calcomanias_tecnicos.xml',
        'views/numeracion_informe.xml',
        'views/numeracion_informe_tecnicos.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}