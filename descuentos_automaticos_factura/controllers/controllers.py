# -*- coding: utf-8 -*-
from odoo import http

# class DescuentosAutomaticosFactura(http.Controller):
#     @http.route('/descuentos_automaticos_factura/descuentos_automaticos_factura/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/descuentos_automaticos_factura/descuentos_automaticos_factura/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('descuentos_automaticos_factura.listing', {
#             'root': '/descuentos_automaticos_factura/descuentos_automaticos_factura',
#             'objects': http.request.env['descuentos_automaticos_factura.descuentos_automaticos_factura'].search([]),
#         })

#     @http.route('/descuentos_automaticos_factura/descuentos_automaticos_factura/objects/<model("descuentos_automaticos_factura.descuentos_automaticos_factura"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('descuentos_automaticos_factura.object', {
#             'object': obj
#         })