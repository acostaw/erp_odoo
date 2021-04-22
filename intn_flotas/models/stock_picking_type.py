# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'


    pedido_materiales_equipos = fields.Boolean(string="Pedido de materiales y/o equipos")
    retiro_materiales_equipos = fields.Boolean(string="Orden de retiro de materiales y/o equipos")

    