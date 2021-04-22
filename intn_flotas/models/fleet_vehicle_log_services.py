# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

class FleetVehicleLogServices(models.Model):
    _inherit = 'fleet.vehicle.log.services'


    next_service_date =fields.Date(string='Fecha del próximo servicio', required=False, track_visibility='onchange')


    next_services_ids = fields.One2many('fleet.vehicle.log.next.services','log_services_id', string="Próximos Servicios")


class FleetVehicleLogNextServices(models.Model):
    _name = 'fleet.vehicle.log.next.services'
    # _rec_name = "workorder_id"

    log_services_id = fields.Many2one('fleet.vehicle.log.services', string='Servicio Padre')
    service_id = fields.Many2one('fleet.service.type',string="Servicio", readonly=False)
    km_aplicado = fields.Integer('KM', readonly=False)
