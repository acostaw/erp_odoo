# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Contratos(models.Model):
    _name = 'intn.contrato'

    name = fields.Char('Número de Contrato', required=True)
    sale_order_id = fields.Many2one('sale.order', string='Expediente', required=True)
    payment_term_id = fields.Many2one('account.payment.term', string='Términos de pago', required=True)
    state = fields.Selection(selection=[('draft', 'Borrador'), ('done', 'Confirmado'), ('canceled', 'Cancelado')],
                             string="Estado", default="draft")
    contrato_pdf = fields.Binary(string="Contrato en PDF")
    pdf_name = fields.Char(string="Contrato en PDF")

    def confirmar_contrato(self):
        for this in self:
            if this.search([('sale_order_id', '=', this.sale_order_id.id), ('state', '=', 'done')]):
                raise ValidationError('Ya existe un contrato validado para éste expediente')
            else:
                this.update({'state': 'done'})
                this.sale_order_id.update({'contrato_id': this.id, 'payment_term_id': this.payment_term_id.id})

    @api.multi
    def unlink(self):
        for this in self:
            if this.state == 'done':
                raise ValidationError('No puede eliminar un contrato confirmada.')
            else:
                super(Contratos, self).unlink()
