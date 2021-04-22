# -*- coding: utf-8 -*-
from odoo import http

# class PresupuestosIntn(http.Controller):
#     @http.route('/presupuestos_intn/presupuestos_intn/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/presupuestos_intn/presupuestos_intn/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('presupuestos_intn.listing', {
#             'root': '/presupuestos_intn/presupuestos_intn',
#             'objects': http.request.env['presupuestos_intn.presupuestos_intn'].search([]),
#         })

#     @http.route('/presupuestos_intn/presupuestos_intn/objects/<model("presupuestos_intn.presupuestos_intn"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('presupuestos_intn.object', {
#             'object': obj
#         })