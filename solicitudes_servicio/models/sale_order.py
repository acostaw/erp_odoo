# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    fecha_estimada = fields.Date(
        string='Fecha estimada de servicio', track_visibility='onchange',
        copy=False)


    solicitud_id = fields.Many2one('solicitudes.servicio', string='Solicitud de Servicio', required=False, index=True, copy=False)

    tecnico_id = fields.Many2one('res.users', string='Técnico asignado', required=False, track_visibility='onchange', related="solicitud_id.tecnico_id")
    bascula_id = fields.Many2one('intn.bascula', string='Bascula', required=False, track_visibility='onchange', related="solicitud_id.bascula_id")
