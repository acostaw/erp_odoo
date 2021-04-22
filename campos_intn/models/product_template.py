# -*- coding: utf-8 -*-

from odoo import models, fields, api


class VerificacionInSitu(models.Model):
    _inherit = "product.template"
    verificacion_insitu = fields.Boolean(string='Se verifica In Situ', default=False)

    organismo_id = fields.Many2one('intn.organismos', string='Organismo', required=False)
    unidad_id = fields.Many2one('intn.unidades', string='Unidad', required=False)
    departamento_id = fields.Many2one('intn.departamentos', string='Departamento', required=False)
    coordinacion_id = fields.Many2one('intn.coordinaciones', string='Coordinación', required=False)
    laboratorio_id = fields.Many2one('intn.laboratorios', string='Laboratorio', required=False)
    determinacion=fields.Char(string="Determinacion")


    @api.multi
    def name_get(self):
        res = super(VerificacionInSitu, self).name_get()
        data = []
        for this in self:
            display_value = this.name
            if this.determinacion:
                display_value += ' - ' + this.determinacion
            data.append((this.id, display_value))
        return data


    @api.onchange('organismo_id')
    def _onChangeOrganismo(self):
        self.unidad_id = False
        self.departamento_id = False
        self.coordinacion_id = False
        self.laboratorio_id = False
        if self.organismo_id:
            return {'domain': {'unidad_id': [('organismo_id', '=', self.organismo_id.id)]}}
        else:
            return {'domain': {'unidad_id': []}}

    @api.onchange('unidad_id')
    def _onChangeUnidad(self):
        self.departamento_id = False
        self.coordinacion_id = False
        self.laboratorio_id = False
        if self.unidad_id:
            return {'domain': {'departamento_id': [('unidad_id', '=', self.unidad_id.id)]}}
        else:
            return {'domain': {'departamento_id': []}}

    @api.onchange('departamento_id')
    def _onChangeDepartamento(self):
        self.coordinacion_id = False
        if self.departamento_id:
            return {'domain': {'coordinacion_id': [('departamento_id', '=', self.departamento_id.id)]}}
        else:
            return {'domain': {'coordinacion_id': []}}

    @api.onchange('laboratoro_id')
    def _onChangeCoordinacion(self):
        self.laboratorio_id = False
        if self.coordinacion_id:
            return {'domain': {'laboratorio_id': [('coordinacion_id', '=', self.coordinacion_id.id)]}}
        else:
            return {'domain': {'laboratorio_id': []}}
