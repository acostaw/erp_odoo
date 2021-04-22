# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    actividad_id = fields.Many2one('actividad.producto', string='Cuenta', track_visibility='onchange')


class ActividadProducto(models.Model):
    _name = 'actividad.producto'

    name = fields.Char('Actividad', required=True)
    active = fields.Boolean('Activo', default=True)
