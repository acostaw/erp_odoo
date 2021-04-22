# -*- coding: utf-8 -*-
from odoo import http

# class UsoMarcaIntn(http.Controller):
#     @http.route('/uso_marca_intn/uso_marca_intn/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/uso_marca_intn/uso_marca_intn/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('uso_marca_intn.listing', {
#             'root': '/uso_marca_intn/uso_marca_intn',
#             'objects': http.request.env['uso_marca_intn.uso_marca_intn'].search([]),
#         })

#     @http.route('/uso_marca_intn/uso_marca_intn/objects/<model("uso_marca_intn.uso_marca_intn"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('uso_marca_intn.object', {
#             'object': obj
#         })