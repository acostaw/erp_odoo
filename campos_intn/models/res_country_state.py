# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class resCountryState(models.Model):
    _inherit = 'res.country.state'


    viatico_monto = fields.Integer('Viatico', related="resolucion_id.monto", store=True)
    departamento_paraguay = fields.Boolean('Departamento_paraguayo', default=False)
    resolucion_id = fields.Many2one('campos_intn.resoluciones_viatico',string="Nro Resolución", domain=[('state', '=', 'done')])
    fecha_vigencia = fields.Datetime(string="Fecha Finalización vigencia",related="resolucion_id.fecha_vigencia")