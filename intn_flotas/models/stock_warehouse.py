# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    user_ids = fields.Many2many('res.users', string="Responsables", required=False)
