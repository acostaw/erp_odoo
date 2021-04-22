# -*- coding: utf-8 -*-

from odoo import models, fields, api


class metodos_pago(models.Model):
    _name = "metodos_pago"
    saleorder_id = fields.Many2one('sale.order')
    sub_etapas = fields.Many2one('uso_marca_sub_etapas')
    monto = fields.Integer("Monto")
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Nota"),
        ('False', "Note")], default='False')
    name = fields.Char("   ")
    sequence = fields.Integer('sequence', default=10)

class metodos_pago_saleorder(models.Model):
     _inherit = 'sale.order'
     # etapas_lines_ids = fields.One2many('etapas','saleorder_id',string='Detalle de Etapas',states={'draft': [('readonly', False)]}, copy=True)
     metodos_pago_ids = fields.One2many('metodos_pago', 'saleorder_id', string='Detalle de Etapas',
                                        states={'draft': [('readonly', False)]}, copy=True)

     product_ids = fields.Many2one('product.product')

     @api.multi
     def bulk_verify(self):
         for record in self:
            print(record)