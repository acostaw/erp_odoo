# -*- coding: utf-8 -*-

from odoo import models, fields, api


class IntnOrganismos(models.Model):
    _inherit = "intn.organismos"

    meta_departamento_ids = fields.One2many('meta.departamentos', 'organismo_id', string='Metas por Departamento', copy=False)

    accion = fields.Char ('Accion', copy=False)
    tareas_especificas = fields.Char ('Tareas Especificas', copy=False)

class MetaDepartamentos(models.Model):
    _name = "meta.departamentos"
    organismo_id = fields.Many2one('intn.organismos')
    state_id = fields.Many2one('res.country.state')
    cantidad = fields.Integer("Cantidad")