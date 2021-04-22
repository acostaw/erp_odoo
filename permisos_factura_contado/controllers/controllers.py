# -*- coding: utf-8 -*-
from odoo import http

# class PermisosFacturaContado(http.Controller):
#     @http.route('/permisos_factura_contado/permisos_factura_contado/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/permisos_factura_contado/permisos_factura_contado/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('permisos_factura_contado.listing', {
#             'root': '/permisos_factura_contado/permisos_factura_contado',
#             'objects': http.request.env['permisos_factura_contado.permisos_factura_contado'].search([]),
#         })

#     @http.route('/permisos_factura_contado/permisos_factura_contado/objects/<model("permisos_factura_contado.permisos_factura_contado"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('permisos_factura_contado.object', {
#             'object': obj
#         })