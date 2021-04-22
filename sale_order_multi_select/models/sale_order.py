# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import datetime,math,locale
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    porcentaje_incremento = fields.Integer(string="% Incremento")

    def seleccionarTodos(self):
        for this in self:
            for line in this.order_line:
                line.select = True

    def eliminarSeleccionados(self):
        for this in self:
            for line in this.order_line:
                if line.select:
                    line.select = False
                    line.unlink()

    def aumentarPrecios(self):
        for this in self:
            for line in this.order_line:
                if line.select:
                    line.price_unit = line.price_unit + (line.price_unit*this.porcentaje_incremento)/100
                    line.select = False

    # @api.multi
    # def write(self, values):
    #     for this in self:
    #         if this._context.get('aumentar') != True:
    #             for line in this.order_line:
    #                 line.select = False

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    select = fields.Boolean(string="X")

