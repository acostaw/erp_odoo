# -*- coding: utf-8 -*-
from odoo import http

# class IntnInformeBascula(http.Controller):
#     @http.route('/intn_informe_bascula/intn_informe_bascula/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/intn_informe_bascula/intn_informe_bascula/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('intn_informe_bascula.listing', {
#             'root': '/intn_informe_bascula/intn_informe_bascula',
#             'objects': http.request.env['intn_informe_bascula.intn_informe_bascula'].search([]),
#         })

#     @http.route('/intn_informe_bascula/intn_informe_bascula/objects/<model("intn_informe_bascula.intn_informe_bascula"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('intn_informe_bascula.object', {
#             'object': obj
#         })