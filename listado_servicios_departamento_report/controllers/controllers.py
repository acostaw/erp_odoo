# -*- coding: utf-8 -*-
from odoo import http

# class FacturasPendientesReport(http.Controller):
#     @http.route('/facturas_pendientes_report/facturas_pendientes_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/facturas_pendientes_report/facturas_pendientes_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('facturas_pendientes_report.listing', {
#             'root': '/facturas_pendientes_report/facturas_pendientes_report',
#             'objects': http.request.env['facturas_pendientes_report.facturas_pendientes_report'].search([]),
#         })

#     @http.route('/facturas_pendientes_report/facturas_pendientes_report/objects/<model("facturas_pendientes_report.facturas_pendientes_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('facturas_pendientes_report.object', {
#             'object': obj
#         })