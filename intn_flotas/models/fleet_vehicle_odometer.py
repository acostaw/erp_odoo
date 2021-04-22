# -*- coding: utf-8 -*-

from odoo import models, api, fields, exceptions


class FleetVehicleOdometer(models.Model):
    _inherit = 'fleet.vehicle.odometer'

    wo_vehicle_id = fields.Many2one('workorder.vehicle', string="Ot Vehiculo", track_visibility='onchange')


class FleetVehicleLogFuel(models.Model):
    _inherit = 'fleet.vehicle.log.fuel'

    wo_vehicle_id = fields.Many2one('workorder.vehicle', string="Ot Vehiculo", track_visibility='onchange')