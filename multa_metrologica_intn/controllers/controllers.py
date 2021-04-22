# -*- coding: utf-8 -*-
from odoo import http

# class MultaMetrologicaIntn(http.Controller):
#     @http.route('/multa_metrologica_intn/multa_metrologica_intn/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/multa_metrologica_intn/multa_metrologica_intn/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('multa_metrologica_intn.listing', {
#             'root': '/multa_metrologica_intn/multa_metrologica_intn',
#             'objects': http.request.env['multa_metrologica_intn.multa_metrologica_intn'].search([]),
#         })

#     @http.route('/multa_metrologica_intn/multa_metrologica_intn/objects/<model("multa_metrologica_intn.multa_metrologica_intn"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('multa_metrologica_intn.object', {
#             'object': obj
#         })