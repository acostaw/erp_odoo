# -*- coding: utf-8 -*-
from odoo import http

# class SolicitudesServicio(http.Controller):
#     @http.route('/solicitudes_servicio/solicitudes_servicio/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/solicitudes_servicio/solicitudes_servicio/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('solicitudes_servicio.listing', {
#             'root': '/solicitudes_servicio/solicitudes_servicio',
#             'objects': http.request.env['solicitudes_servicio.solicitudes_servicio'].search([]),
#         })

#     @http.route('/solicitudes_servicio/solicitudes_servicio/objects/<model("solicitudes_servicio.solicitudes_servicio"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('solicitudes_servicio.object', {
#             'object': obj
#         })