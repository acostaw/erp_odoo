# -*- coding: utf-8 -*-
{
    'name': "INTN Flotas",

    'summary': """
        Se agrega el registro de flotas""",

    'description': """
        Se agrega el registro de flotas"
    """,

    'author': "Interfaces S.A",
    'website': "http://www.interfaces.com.py",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Fleet',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','fleet','campos_intn','stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/res_partner.xml',
        'views/categoria_registros.xml',
        'views/fleet_vehicle_log_services.xml',
        'views/fleet_vehicle.xml',
        'views/informe_provisional_averia.xml',
        'views/solicitud_trabajo.xml',
        'views/solicitud_trabajo_report.xml',
        'views/habilitacion_choferes.xml',
        #'views/workorder_vehicle.xml',
        'views/workorder_vehicle_report.xml',
        'views/devolucion_vehiculo.xml',
        'views/devolucion_vehiculo_report.xml',
        'views/stock_warehouse.xml',
        'views/stock_picking.xml',
        'views/stock_picking_type.xml',
        'views/pedido_materiales_equipos.xml',
        'views/retiro_materiales_equipos.xml',
        'views/informe_pipa.xml',
        'views/fleet_vehicle_odometer.xml',
        'views/sale_order.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}