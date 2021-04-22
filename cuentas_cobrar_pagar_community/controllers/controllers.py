# -*- coding: utf-8 -*-
from odoo import http

# class CuentasCobrarPagarCommunity(http.Controller):
#     @http.route('/cuentas_cobrar_pagar_community/cuentas_cobrar_pagar_community/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cuentas_cobrar_pagar_community/cuentas_cobrar_pagar_community/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cuentas_cobrar_pagar_community.listing', {
#             'root': '/cuentas_cobrar_pagar_community/cuentas_cobrar_pagar_community',
#             'objects': http.request.env['cuentas_cobrar_pagar_community.cuentas_cobrar_pagar_community'].search([]),
#         })

#     @http.route('/cuentas_cobrar_pagar_community/cuentas_cobrar_pagar_community/objects/<model("cuentas_cobrar_pagar_community.cuentas_cobrar_pagar_community"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cuentas_cobrar_pagar_community.object', {
#             'object': obj
#         })