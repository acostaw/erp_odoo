# -*- coding: utf-8 -*-

from odoo import models, api, fields, exceptions


class HabilitacionChoferes(models.Model):
    _name = 'habilitacion.choferes'
    _description = 'Choferes habilitados segun resolucion'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _rec_name = 'year'

    @api.model
    def year_selection(self):
        year = 2021  # replace 2000 with your a start year
        year_list = []
        while year != 2030:  # replace 2030 with your end year
            year_list.append((str(year), str(year)))
            year += 1
        return year_list

    year = fields.Selection(year_selection, string='Año', store=True, required=True, track_visibility='onchange')

    nro_resolucion = fields.Char('N° de Resolución', required=True, track_visibility='onchange')

    driver_id = fields.Many2one('res.partner',string='Chofer',required=True, track_visibility='onchange')

    active= fields.Boolean('Activo', default=True, track_visibility='onchange')
