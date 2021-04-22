# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import datetime,math,locale
from odoo.exceptions import ValidationError

class AccountInvoice(models.Model):
    _inherit = "account.invoice"


    def seleccionarTodos(self):
        for this in self:
            for line in this.invoice_line_ids:
                line.select = True

    def eliminarSeleccionados(self):
        for this in self:
            for line in this.invoice_line_ids:
                if line.select:
                    line.select = False
                    line.unlink()


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    select = fields.Boolean(string="X")
