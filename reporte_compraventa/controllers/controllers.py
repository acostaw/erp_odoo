# -*- coding: utf-8 -*-
from odoo import http

# class ReporteCompraventa(http.Controller):
#     @http.route('/reporte_compraventa/reporte_compraventa/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/reporte_compraventa/reporte_compraventa/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('reporte_compraventa.listing', {
#             'root': '/reporte_compraventa/reporte_compraventa',
#             'objects': http.request.env['reporte_compraventa.reporte_compraventa'].search([]),
#         })

#     @http.route('/reporte_compraventa/reporte_compraventa/objects/<model("reporte_compraventa.reporte_compraventa"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('reporte_compraventa.object', {
#             'object': obj
#         })