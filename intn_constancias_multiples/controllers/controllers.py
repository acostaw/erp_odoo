# -*- coding: utf-8 -*-
from odoo import http

# class IntnConstanciasMultiples(http.Controller):
#     @http.route('/intn_constancias_multiples/intn_constancias_multiples/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/intn_constancias_multiples/intn_constancias_multiples/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('intn_constancias_multiples.listing', {
#             'root': '/intn_constancias_multiples/intn_constancias_multiples',
#             'objects': http.request.env['intn_constancias_multiples.intn_constancias_multiples'].search([]),
#         })

#     @http.route('/intn_constancias_multiples/intn_constancias_multiples/objects/<model("intn_constancias_multiples.intn_constancias_multiples"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('intn_constancias_multiples.object', {
#             'object': obj
#         })