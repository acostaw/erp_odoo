# -*- coding: utf-8 -*-
from odoo import http

# class IntnInteresesMora(http.Controller):
#     @http.route('/intn_intereses_mora/intn_intereses_mora/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/intn_intereses_mora/intn_intereses_mora/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('intn_intereses_mora.listing', {
#             'root': '/intn_intereses_mora/intn_intereses_mora',
#             'objects': http.request.env['intn_intereses_mora.intn_intereses_mora'].search([]),
#         })

#     @http.route('/intn_intereses_mora/intn_intereses_mora/objects/<model("intn_intereses_mora.intn_intereses_mora"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('intn_intereses_mora.object', {
#             'object': obj
#         })