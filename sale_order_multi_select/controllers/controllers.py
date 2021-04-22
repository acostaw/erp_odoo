# -*- coding: utf-8 -*-
# from odoo import http


# class TallerMultiSelect(http.Controller):
#     @http.route('/taller_multi_select/taller_multi_select/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/taller_multi_select/taller_multi_select/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('taller_multi_select.listing', {
#             'root': '/taller_multi_select/taller_multi_select',
#             'objects': http.request.env['taller_multi_select.taller_multi_select'].search([]),
#         })

#     @http.route('/taller_multi_select/taller_multi_select/objects/<model("taller_multi_select.taller_multi_select"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('taller_multi_select.object', {
#             'object': obj
#         })
