# -*- coding: utf-8 -*-

from odoo import models, api, fields, exceptions
from odoo.exceptions import ValidationError

class SolicitudTrabajo(models.Model):
    _name = 'solicitud.trabajo'
    _description = 'Solicitud Interna de trabajo'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char('Número', default="Borrador")

    date = fields.Date(string="Fecha", required=True, default=fields.Date.today,track_visibility='onchange')
    organismo_solicitante_id = fields.Many2one('intn.organismos', string="Organismo Solicitante", required=True,track_visibility='onchange')
    unidad_solicitante_id = fields.Many2one('intn.unidades',string="Unidad Solicitante",track_visibility='onchange', required=True)
    dpto_solicitante_id = fields.Many2one('intn.departamentos',string="Departamento Solicitante",track_visibility='onchange', required=True)
    organismo_receptor_id = fields.Many2one('intn.organismos', string="Organismo Receptor", required=True,track_visibility='onchange')
    unidad_receptor_id = fields.Many2one('intn.unidades',string="Unidad Receptor",track_visibility='onchange', required=True)
    dpto_receptor_id = fields.Many2one('intn.departamentos',string="Departamento Receptor",track_visibility='onchange', required=True)
    descripcion = fields.Html(required=True, string= "Descripción de lo solicitado",track_visibility='onchange')

    currency_id = fields.Many2one(
        'res.currency', default=lambda self: self.env.user.company_id.currency_id)

    responsable_receptor = fields.Many2one('res.users', 'Realizado por', required=False,track_visibility='onchange')
    fecha_recepcion = fields.Date(string="Fecha de Recepcion", track_visibility='onchange')
    costo_aprox = fields.Monetary('Costo aprox.',track_visibility='onchange')
    talonario_pedido_id = fields.Many2one('stock.picking',string='Talonario de pedido n°:',track_visibility='onchange')
    talonario_retiro_id = fields.Many2one('stock.picking',string='Talonario de retiro n°:',track_visibility='onchange')


    realizado = fields.Selection(string='Realizado', selection=[('si', 'Si'), ('no', 'No')],track_visibility='onchange')
    realizado_por = fields.Many2one('res.users', 'Realizado por', required=False,track_visibility='onchange')
    fecha_realizacion = fields.Date(string="Fecha de Realizacion", track_visibility='onchange')
    motivo_no_realizado = fields.Char(string="Motivo",track_visibility='onchange')
    observaciones = fields.Text(string="Observacions y/o comentarios",track_visibility='onchange')

    pipa_id = fields.Many2one('informe.provisional.averia', string='Informe Provisional de Avería en institucional (P.I.P.A.)')

    state = fields.Selection(string='Estado', selection=[(
        'draft', 'Borrador'), ('done', 'Confirmado'), ('cancel', 'Cancelado')], default='draft',
                             track_visibility='onchange')

    def genera_secuencia(self):
        for this in self:
            seq = self.sudo().env['ir.sequence'].next_by_code('seq_wo_vehicle')
            if seq:
                return seq

    def asigna_nombre(self):
        for i in self:
            if self.name and self.name == 'Borrador':
                new_name = i.genera_secuencia()
                i.write({'name': new_name})
            else:
                return

    @api.onchange('organismo_solicitante_id')
    def _onChangeOrganismoSolicitante(self):
        self.unidad_solicitante_id = False
        self.dpto_solicitante_id = False
        if self.organismo_solicitante_id:
            return {'domain': {'unidad_solicitante_id': [('organismo_id', '=', self.organismo_solicitante_id.id)]}}
        else:
            return {'domain': {'unidad_solicitante_id': []}}

    @api.onchange('unidad_solicitante_id')
    def _onChangeUnidadSolicitante(self):
        self.dpto_solicitante_id = False
        if self.unidad_solicitante_id:
            return {'domain': {'dpto_solicitante_id': [('unidad_id', '=', self.unidad_solicitante_id.id)]}}
        else:
            return {'domain': {'dpto_solicitante_id': []}}

    @api.onchange('organismo_receptor_id')
    def _onChangeOrganismoReceptor(self):
        self.unidad_receptor_id = False
        self.dpto_receptor_id = False
        if self.organismo_receptor_id:
            return {'domain': {'unidad_receptor_id': [('organismo_id', '=', self.organismo_receptor_id.id)]}}
        else:
            return {'domain': {'unidad_receptor_id': []}}

    @api.onchange('unidad_receptor_id')
    def _onChangeUnidadReceptor(self):
        self.dpto_receptor_id = False
        if self.unidad_receptor_id:
            return {'domain': {'dpto_receptor_id': [('unidad_id', '=', self.unidad_receptor_id.id)]}}
        else:
            return {'domain': {'dpto_receptor_id': []}}


    def button_confirmar(self):
        for i in self:
            i.asigna_nombre()
            i.write({'state': 'done'})

    def button_cancelar(self):
        for i in self:
            i.write({'state': 'cancel'})