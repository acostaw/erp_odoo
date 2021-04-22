# -*- coding: utf-8 -*-

from odoo import models, api, fields, exceptions
import qrcode
import base64
import hashlib
from io import BytesIO
from odoo.exceptions import ValidationError
import datetime


class TipoConstancias(models.Model):
    _name = 'tipo.constancias'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Tipo de Constancia', required=True)

    plantilla_id = fields.Many2one('plantilla.constancias', string="Plantilla de Constancias", required=True)

    cuerpo = fields.Html(string="Cuerpo de la constancia")

    # Fake fields used to implement the placeholder assistant

    model_object_field = fields.Many2one('ir.model.fields', string="Campo")
    sub_object = fields.Many2one('ir.model', 'Sub-modelo', readonly=True)
    sub_model_object_field = fields.Many2one('ir.model.fields', 'Sub-campo')
    null_value = fields.Char('Valor por defecto')
    copyvalue = fields.Char('Expresión de marcador')
    model_id = fields.Many2one('ir.model', 'Modelo', default=lambda self: self.env['ir.model'].search([('model', '=', 'constancias.multiples')]))


    @api.onchange('plantilla_id')
    def onchangePlantilla(self):
        if self.plantilla_id:
            campos = self.mapped('plantilla_id.fields_ids.fields_id')
            campos = campos.mapped('id')
            return {'domain': {'model_object_field': [('id', 'in', campos)]}}
        else:
            return {'domain': {'model_object_field': []}}

    @api.onchange('model_id')
    def onchange_model_id(self):
        if self.model_id:
            self.model = self.model_id.model
        else:
            self.model = False

    def build_expression(self, field_name, sub_field_name, null_value):
        """Returns a placeholder expression for use in a template field,
        based on the values provided in the placeholder assistant.

        :param field_name: main field name
        :param sub_field_name: sub field name (M2O)
        :param null_value: default value if the target value is empty
        :return: final placeholder expression """
        expression = ''
        if field_name:
            expression = "{{" + field_name
            if sub_field_name:
                expression += "#" + sub_field_name
            if null_value:
                expression += " or '''%s'''" % null_value
            expression += "}}"
        return expression

    @api.onchange('model_object_field', 'sub_model_object_field', 'null_value')
    def onchange_sub_model_object_value_field(self):
        if self.model_object_field:
            if self.model_object_field.ttype in ['many2one', 'one2many', 'many2many']:
                model = self.env['ir.model']._get(self.model_object_field.relation)
                if model:
                    self.sub_object = model.id
                    self.copyvalue = self.build_expression(self.model_object_field.name,
                                                           self.sub_model_object_field and self.sub_model_object_field.name or False,
                                                           self.null_value or False)
            else:
                self.sub_object = False
                self.sub_model_object_field = False
                self.copyvalue = self.build_expression(self.model_object_field.name, False, self.null_value or False)
        else:
            self.sub_object = False
            self.copyvalue = False
            self.sub_model_object_field = False
            self.null_value = False