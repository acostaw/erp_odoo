# -*- coding: utf-8 -*-

from odoo import models, fields, api


class IntnWorkCenter(models.Model):
    _inherit = "mrp.workcenter"
    _rec_name = 'complete_name'

    complete_name = fields.Char(string='Nombre', compute='completeNameWorkCenter')

    def completeNameWorkCenter(self):
        for this in self:
            laboratorio = self.env['intn.laboratorios'].search([('mrp_workcenter_id', '=', this.id)])
            if laboratorio:
                this.complete_name = laboratorio.complete_name
            else:
                coordinacion = self.env['intn.coordinaciones'].search([('mrp_workcenter_id', '=', this.id)])
                if coordinacion:
                    this.complete_name = coordinacion.complete_name
                else:
                    departamento = self.env['intn.departamentos'].search([('mrp_workcenter_id', '=', this.id)])
                    if departamento:
                        this.complete_name = departamento.complete_name
                    else:
                        unidad = self.env['intn.unidades'].search([('mrp_workcenter_id', '=', this.id)])
                        if unidad   :
                            this.complete_name = unidad.complete_name
                        else:
                            organismo = self.env['intn.organismos'].search([('mrp_workcenter_id', '=', this.id)])
                            if organismo:
                                this.complete_name = organismo.name
                            else:
                                this.complete_name = this.name