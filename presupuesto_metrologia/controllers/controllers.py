# -*- coding: utf-8 -*-
from odoo import http

# class PresupuestoMetrologia(http.Controller):
#     @http.route('/presupuesto_metrologia/presupuesto_metrologia/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/presupuesto_metrologia/presupuesto_metrologia/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('presupuesto_metrologia.listing', {
#             'root': '/presupuesto_metrologia/presupuesto_metrologia',
#             'objects': http.request.env['presupuesto_metrologia.presupuesto_metrologia'].search([]),
#         })

#     @http.route('/presupuesto_metrologia/presupuesto_metrologia/objects/<model("presupuesto_metrologia.presupuesto_metrologia"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('presupuesto_metrologia.object', {
#             'object': obj
#         })