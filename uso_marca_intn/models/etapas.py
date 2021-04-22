# -*- coding: utf-8 -*-

from odoo import models, fields, api

class nombre_etapas(models.Model):
    _name = "uso_marca_nombre_etapas"
    name = fields.Char()

class sub_etapas(models.Model):
    _name = "uso_marca_sub_etapas"
    name = fields.Char()

class etapas(models.Model):
    _name = "etapas"
    saleorder_id = fields.Many2one('sale.order')
    etapas = fields.Many2one('uso_marca_nombre_etapas')
    sub_etapas = fields.Many2one('uso_marca_sub_etapas')
    duracion = fields.Char("Duracion/Frecuencia")
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Nota"),
        ('False', "Note")], default='False')
    name = fields.Char("   ")
    sequence = fields.Integer('sequence', default=10)

class etapas_saleorder(models.Model):
     _inherit = 'sale.order'
     etapas_lines_ids = fields.One2many('etapas','saleorder_id',string='Detalle de Etapas',states={'draft': [('readonly', False)]}, copy=True)