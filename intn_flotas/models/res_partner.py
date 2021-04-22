# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import models, fields, api, exceptions


class ResPartner(models.Model):
    _inherit = 'res.partner'


    es_chofer = fields.Boolean('Es chofer', track_visibility='onchange')

    ci_num = fields.Char('C.I.')

    nro_registro = fields.Char('Nro de registro')

    municipio = fields.Char('Municipio')

    categoria_registro_id = fields.Many2one('categoria.registros', string="Categoria")

    chofer_habilitado = fields.Boolean(string="Chofer habilitado", compute="computeChoferHabilitado")


    def computeChoferHabilitado(self):
        for this in self:
            today = datetime.datetime.now()
            year = today.year
            habilitacion_chofer = self.env['habilitacion.choferes'].search([('partner_id', '=', this.id),('active','=',True),('year','=',year)])
            if habilitacion_chofer:
                this.chofer_habilitado = True
            else:
                this.chofer_habilitado = False

class CategoriaRegistros(models.Model):
    _name = 'categoria.registros'
    name = fields.Char('Nombre')

    active= fields.Boolean('Activo', default=True)
