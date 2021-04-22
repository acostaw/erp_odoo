# -*- coding: utf-8 -*-
from odoo import http

# class StandardRuc(http.Controller):
#     @http.route('/standard_ruc/standard_ruc/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/standard_ruc/standard_ruc/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('standard_ruc.listing', {
#             'root': '/standard_ruc/standard_ruc',
#             'objects': http.request.env['standard_ruc.standard_ruc'].search([]),
#         })

#     @http.route('/standard_ruc/standard_ruc/objects/<model("standard_ruc.standard_ruc"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('standard_ruc.object', {
#             'object': obj
#         })