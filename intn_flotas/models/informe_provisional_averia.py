# -*- coding: utf-8 -*-

from odoo import models, api, fields, exceptions


class InformeProvisionalAveria(models.Model):
    _name = 'informe.provisional.averia'
    _description = 'Informe Provisional de Avería en institucional (P.I.P.A.)'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Número', default="Borrador")

    driver_id = fields.Many2one('res.partner', string="De", related="vehicle_id.driver_id", required=True,
                                readonly=False, track_visibility=True)

    #user_id = fields.Many2one('res.users', 'De',
    #                         default=lambda self: self.env.user, required=True,track_visibility='onchange')
    organismo_id = fields.Many2one('intn.organismos', string="Organismo", required=True,track_visibility='onchange')
    unidad_id = fields.Many2one('intn.unidades',string="Unidad",track_visibility='onchange', required=True)
    date = fields.Date(string="Fecha", required=True, default=fields.Date.today,track_visibility='onchange')
    vehicle_id = fields.Many2one('fleet.vehicle',string="Vehiculo", required=True,track_visibility='onchange')
    km_actual = fields.Integer('Kilometraje actual', required=True,track_visibility='onchange')

    wo_vehicle_id = fields.Many2one('workorder.vehicle',string="Ot Vehiculo",track_visibility='onchange')
    vigencia_desde = fields.Date(string="Vigencia desde", required=True,track_visibility='onchange', related="wo_vehicle_id.fecha_inicio")
    vigencia_hasta = fields.Date(string="Vigencia hasta", required=True,track_visibility='onchange', related="wo_vehicle_id.fecha_fin")
    descripcion_averia = fields.Html('Breve descripcion de la averia', required=True,track_visibility='onchange')

    state = fields.Selection(string='Estado', selection=[(
        'draft', 'Borrador'), ('done', 'Confirmado'), ('cancel', 'Cancelado')], default='draft',
                             track_visibility='onchange')

    def genera_secuencia(self):
        for this in self:
            seq = self.sudo().env['ir.sequence'].next_by_code('seq_pipa')
            if seq:
                return seq

    def asigna_nombre(self):
        for i in self:
            if self.name and self.name == 'Borrador':
                new_name = i.genera_secuencia()
                i.write({'name': new_name})
            else:
                return

    @api.onchange('organismo_id')
    def _onChangeOrganismo(self):
        self.unidad_id = False
        if self.organismo_id:
            return {'domain': {'unidad_id': [('organismo_id', '=', self.organismo_id.id)]}}
        else:
            return {'domain': {'unidad_id': []}}

    def button_confirmar(self):
        for i in self:
            i.asigna_nombre()
            i.write({'state': 'done'})

    def button_cancelar(self):
        for i in self:
            i.write({'state': 'cancel'})


    def solicitud_interna_trabajo(self):
        self.ensure_one()
        return {
            'name': ('Solicitud Interna de Trabajo'),
            'res_model': 'solicitud.trabajo',
            'type': 'ir.actions.act_window',
            'views': [(False, 'list'), (False, 'form')],
            'view_mode': 'list, form',
            'context': {
                "default_pipa_id": self.id,
                "search_default_pipa_id": self.id,
                # "group_by": 'sale_order_id'
            },
        }