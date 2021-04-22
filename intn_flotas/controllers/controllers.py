# -*- coding: utf-8 -*-
from odoo import http

# class IntnFlotas(http.Controller):
#     @http.route('/intn_flotas/intn_flotas/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/intn_flotas/intn_flotas/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('intn_flotas.listing', {
#             'root': '/intn_flotas/intn_flotas',
#             'objects': http.request.env['intn_flotas.intn_flotas'].search([]),
#         })

#     @http.route('/intn_flotas/intn_flotas/objects/<model("intn_flotas.intn_flotas"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('intn_flotas.object', {
#             'object': obj
#         })