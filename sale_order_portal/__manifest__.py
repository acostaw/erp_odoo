# -*- coding: utf-8 -*-
{
    'name': "Presupuesto Portal",

    'summary': """
        Se modifica la vista de Presupuesto desde el Portal de Clientes""",

    'description': """
        Se modifica la vista de Presupuesto desde el Portal de Clientes
    """,

    'author': "Interfaces S.A",
    'website': "http://www.interfaces.com.py",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Portal',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','presupuestos_intn','portal','sale','account','factura_autoimpresor','intn_constancias_multiples'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/sale_order_portal.xml',
        'views/portal_invoice_page.xml',
        'views/portal_my_home_sale.xml',
        'views/portal_my_invoices.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}