# -*- coding: utf-8 -*-

from odoo import models, api, fields, exceptions
from lxml import etree
#
# class IrModelFields(models.Model):
#     _inherit = 'ir.model.fields'
#
#     plantilla_constancia_id = fields.Many2one('plantila.constancias')


class PlantillaConstancias(models.Model):
    _name = 'plantilla.constancias'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Nombre de la Plantilla', required=True)

    fields_ids = fields.One2many('plantilla.constancias.line','plantilla_constancia_id', string="Campos", required=True)

    model_id = fields.Many2one('ir.model', string="Modelo", compute="getModelo")

    @api.depends('fields_ids')
    def getModelo(self):
        for this in self:
            model_id = self.env['ir.model'].search([('model', '=', 'constancias.multiples')])
            this.model_id = model_id


class PlantillaConstanciasLine(models.Model):
    _name = 'plantilla.constancias.line'

    plantilla_constancia_id = fields.Many2one('plantilla.constancias',string="Plantilla de Constancias", required=True)

    sequence=fields.Integer('Secuencia', default=10)

    fields_id = fields.Many2one('ir.model.fields',string="Campos", required=True)

    field_description = fields.Char('Descripcion',related="fields_id.field_description")

    model_id = fields.Many2one('ir.model', string="Modelo", related="fields_id.model_id")

    ttype=fields.Selection(string="Tipo", related="fields_id.ttype")


#
#
