# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    aparece_solicitudes_servicio = fields.Boolean('Aparece en las solicitudes de Servicio', default=False)
