# -*- coding: utf-8 -*-
from odoo import http

# class PermisosFacturacion(http.Controller):
#     @http.route('/permisos_facturacion/permisos_facturacion/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/permisos_facturacion/permisos_facturacion/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('permisos_facturacion.listing', {
#             'root': '/permisos_facturacion/permisos_facturacion',
#             'objects': http.request.env['permisos_facturacion.permisos_facturacion'].search([]),
#         })

#     @http.route('/permisos_facturacion/permisos_facturacion/objects/<model("permisos_facturacion.permisos_facturacion"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('permisos_facturacion.object', {
#             'object': obj
#         })