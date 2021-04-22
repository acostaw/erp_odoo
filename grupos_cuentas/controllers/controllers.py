# -*- coding: utf-8 -*-
from odoo import http

# class InterfacesPlanCuentas(http.Controller):
#     @http.route('/interfaces_plan_cuentas/interfaces_plan_cuentas/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/interfaces_plan_cuentas/interfaces_plan_cuentas/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('interfaces_plan_cuentas.listing', {
#             'root': '/interfaces_plan_cuentas/interfaces_plan_cuentas',
#             'objects': http.request.env['interfaces_plan_cuentas.interfaces_plan_cuentas'].search([]),
#         })

#     @http.route('/interfaces_plan_cuentas/interfaces_plan_cuentas/objects/<model("interfaces_plan_cuentas.interfaces_plan_cuentas"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('interfaces_plan_cuentas.object', {
#             'object': obj
#         })