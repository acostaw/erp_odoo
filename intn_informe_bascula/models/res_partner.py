# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    bascula_ids = fields.Many2many('intn.bascula', string="Básculas", copy=False, track_visibility=True)

    basculas= fields.Html(compute='getBasculas',string='Basculas')
    basculas_publico = fields.Html(compute='getBasculasPublico',string='Basculas Publico')


    def get_selection_label(self, object, field_name, field_value):
        return _(dict(self.env[object].fields_get(allfields=[field_name])[field_name]['selection'])[field_value])

    def getBasculas(self):
        for this in self:
            table = "<table style='width:100%;font-size:10px;text-align:center;font-weight:bold'>" \
                   "<tr> " \
                   "<td> Báscula </td><td> Fecha de verificacion </td> <td> Fecha de vencimiento </td> <td> Estado </td></tr>"
            if this.bascula_ids:
                for bascula in this.bascula_ids:
                    state_value = dict(bascula._fields['state'].selection).get(bascula.state)
                    if bascula.name:
                        table = table + "<tr style='color:black;background:"+ str(bascula.color) + "'>"
                        table = table + "<td>" + str(bascula.name)
                    if bascula.fecha_verificacion:
                        table = table +"</td><td>" + str(bascula.fecha_verificacion.strftime("%d-%m-%Y"))
                    if bascula.fecha_vencimiento:
                        table = table + "</td><td>" + str(bascula.fecha_vencimiento.strftime("%d-%m-%Y"))
                    if state_value:
                        table = table + "</td><td>"+ str(state_value) + "</td>"
                    table = table + "</tr>"
                table = table + '</table>'
                this.basculas = table

    def getBasculasPublico(self):
        for this in self:
            table = "<table style='width:100%;font-size:10px;text-align:center;font-weight:bold'>" \
                    "<tr> " \
                    "<td> Báscula </td><td> Estado </td></tr>"
            if this.bascula_ids:
                for bascula in this.bascula_ids:
                    state_value = dict(bascula._fields['state'].selection).get(bascula.state)
                    # state_value = self.get_selection_label(self,'intn.bascula', 'state', bascula.state)
                    if bascula.name:
                        table = table + "<tr style='color:black;background:" + str(bascula.color) + "'>"
                        table = table + "<td>" + str(bascula.name)
                    if state_value:
                        table = table + "</td><td>" + str(state_value) + "</td>"
                    table = table + "</tr>"
                table = table + "</table>"
                this.basculas_publico = table
