# -*- coding: utf-8 -*-
from odoo import http

# class CamposIntn(http.Controller):
#     @http.route('/campos_intn/campos_intn/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/campos_intn/campos_intn/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('campos_intn.listing', {
#             'root': '/campos_intn/campos_intn',
#             'objects': http.request.env['campos_intn.campos_intn'].search([]),
#         })

#     @http.route('/campos_intn/campos_intn/objects/<model("campos_intn.campos_intn"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('campos_intn.object', {
#             'object': obj
#         })