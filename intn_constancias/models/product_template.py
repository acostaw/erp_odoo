# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"


    secuencia_constancia = fields.Many2one('ir.sequence',string='Secuencia de Constancia')