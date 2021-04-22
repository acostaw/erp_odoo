# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError
from datetime import datetime
from dateutil.relativedelta import relativedelta


class accountInvoice(models.Model):
    _inherit = 'account.invoice'

    monto_interes = fields.Monetary(
        'Intereses Acumulados', compute='_get_intereses_acumulados', copy=False)
    factura_mora = fields.Many2one(
        'account.invoice', string='Factura mora', copy=False)
    factura_origen_mora = fields.Many2one(
        'account.invoice', string='Factura origen', copy=False)

    facturas_origen_mora = fields.Many2many('account.invoice', 'facturas_origen_multiples', 'id', 'facturas_origen_mora',
                                            string="Facturas Origen", copy=False)

    dias_atraso = fields.Integer(
        string="Días de atraso", compute="_get_intereses_acumulados", copy=False)
    desactivar_mora = fields.Boolean(default=False, copy=False)

    interes_diario_base = fields.Monetary(
        string="Interés por Dia", compute='_get_intereses_acumulados', copy=False)

    def button_wizard_pago(self):
        if self.type == 'out_invoice':
            view = self.env.ref('intn_intereses_mora.wizard_pago_form')
            return{
                'name': 'Registrar pago de intereses',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'intn_intereses_mora.wizard_pago',
                'context': {'default_factura_origen': self.id},
                'view_id': view.id,
                'target': 'new',
            }

    def get_factura_mora_pagada(self):
        for i in self:
            if (i.factura_mora and i.factura_mora.state == 'paid' and i.factura_mora.state != 'cancel') or i.desactivar_mora or i.partner_id.es_entidad_estado:
                return True
            return False

    @api.model
    def calcular_intereses(self, invoice, date_payment):
        dias_atraso = (date_payment-invoice.date_due).days
        fecha_exonerada=datetime.strptime('2017-01-01','%Y-%m-%d').date()
        if invoice.date_due < fecha_exonerada:
            dias_atraso = 0
        if dias_atraso > 0 and not invoice.get_factura_mora_pagada():
            porcentaje_mensual = float(
                self.sudo().env['ir.config_parameter'].get_param('interes_mora_parameter'))
            interes_mensual_base = invoice.amount_total_company_signed * porcentaje_mensual/100
            interes_diario_base = float(interes_mensual_base/30)
            interes = dias_atraso*interes_diario_base
            return{
                'interes': interes,
                'dias_atraso': dias_atraso,
                'interes_diario_base': interes_diario_base
            }
        else:
            return{
                'interes': 0,
                'dias_atraso': 0
            }

    def _get_intereses_acumulados(self):
        for invoice in self:
            if invoice.state == 'open':
                data = invoice.calcular_intereses(
                    invoice, date_payment=fields.Date.today())
                invoice.monto_interes = data.get('interes')
                invoice.dias_atraso = data.get('dias_atraso')
                invoice.interes_diario_base = data.get('interes_diario_base')
            else:
                invoice.monto_interes = 0
                invoice.dias_atraso = 0

    def button_pago(self):
        for i in self:
            if i.monto_interes > 0:
                raise exceptions.ValidationError(
                    'No se puede registrar un pago a una factura con intereses por mora. Primero registre la factura de la mora')
            return super(accountInvoice, i).button_pago()

    @api.model
    def button_pago_multi(self, facturas):
        for i in facturas:
            if i.monto_interes > 0:
                raise exceptions.ValidationError(
                    'No se puede registrar un pago a una factura con intereses por mora. Primero registre la factura de la mora')
            return super(accountInvoice, i).button_pago_multi(facturas)

    @api.model
    def button_pago_multi_intereses(self, facturas):
        if facturas[0].type == 'out_invoice':
            flag = self.env.user.has_group(
                'intn_intereses_mora.grupo_facturas_mora')
            if flag:
                view = self.env.ref('intn_intereses_mora.wizard_pago_form')
                return {
                    'name': 'Registrar pago de intereses',
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'intn_intereses_mora.wizard_pago',
                    'context': {'default_facturas_origen': [(6, 0, facturas.ids)]},
                    'view_id': view.id,
                    'target': 'new',
                }
            else:
                raise UserError(
                    'Su usuario no cuenta con permisos para registrar facturas por mora')
