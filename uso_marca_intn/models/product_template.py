# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"
    etapas = fields.Selection([
        ('etapa_inicial', "Etapa Inicial"),
        ('etapa_uno', "Etapa I"),
        ('etapa_dos', "Etapa II"),
        ('etapa_tres','Etapa III'),
        ('etapa_vigilancia','Etapa de Vigilancia')],required=False, default=False)