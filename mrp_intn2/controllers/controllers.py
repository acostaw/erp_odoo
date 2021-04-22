# -*- coding: utf-8 -*-
from odoo import http

# class MrpIntn2(http.Controller):
#     @http.route('/mrp_intn2/mrp_intn2/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mrp_intn2/mrp_intn2/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mrp_intn2.listing', {
#             'root': '/mrp_intn2/mrp_intn2',
#             'objects': http.request.env['mrp_intn2.mrp_intn2'].search([]),
#         })

#     @http.route('/mrp_intn2/mrp_intn2/objects/<model("mrp_intn2.mrp_intn2"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mrp_intn2.object', {
#             'object': obj
#         })