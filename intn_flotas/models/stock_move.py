# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = "stock.move"

    actividad_id = fields.Many2one('actividad.producto',string='Cuenta', track_visibility='onchange')
