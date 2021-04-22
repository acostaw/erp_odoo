# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    es_entidad_estado = fields.Boolean(string='Es una Entidad del Estado', default=False, track_visibility='onchange')
    es_extranjero = fields.Boolean(string='Es un cliente extranjero', default=False, track_visibility='onchange')
