# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import datetime
from dateutil.relativedelta import relativedelta


class accountInvoice(models.Model):
    _inherit = 'account.invoice'

    multa_origen = fields.Many2one(
        'multa_metrologica_intn', string='Resolucion por multa metrologica de Origen')

    def action_invoice_open(self):
        for this in self:
            if this.multa_origen:
                this.multa_origen.write({'state': 'done'})
            return super(accountInvoice, self).action_invoice_open()