# -*- coding: utf-8 -*-
from odoo import http

# class ReporteServiciosJerarquia(http.Controller):
#     @http.route('/reporte_servicios_jerarquia/reporte_servicios_jerarquia/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/reporte_servicios_jerarquia/reporte_servicios_jerarquia/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('reporte_servicios_jerarquia.listing', {
#             'root': '/reporte_servicios_jerarquia/reporte_servicios_jerarquia',
#             'objects': http.request.env['reporte_servicios_jerarquia.reporte_servicios_jerarquia'].search([]),
#         })

#     @http.route('/reporte_servicios_jerarquia/reporte_servicios_jerarquia/objects/<model("reporte_servicios_jerarquia.reporte_servicios_jerarquia"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('reporte_servicios_jerarquia.object', {
#             'object': obj
#         })