# -*- coding: utf-8 -*-

from odoo import models, api, fields, exceptions,_
from odoo.exceptions import ValidationError
from datetime import date


class WorkorderVehicle(models.Model):
    _name = 'workorder.vehicle'
    _description = 'Orden de Trabajo'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'nro_orden'

    state = fields.Selection(string='Estado', selection=[(
        'open', 'Abierto'), ('closed', 'Cerrado'), ('cancel', 'Cancelado')], default='open',
                             track_visibility='onchange')

    order_id = fields.Many2one('sale.order', string='Expediente', required=True, track_visibility='onchange')

    companion_ids = fields.Many2many('res.partner', string="Acompañantes")


    wo_type = fields.Selection(string='Tipo', selection=[(
        'ordinary', 'Ordinario'), ('extraordinary', 'Extraordinario')], default='ordinary',
                             track_visibility='onchange')

    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehiculo", required=True,track_visibility=True)

    driver_id = fields.Many2one('res.partner', string="Conductor", related="vehicle_id.driver_id",required=True, readonly=False, track_visibility=True)
    fuel_type = fields.Selection([
        ('gasoline', 'Gasolina'),
        ('diesel', 'Diesel'),
        ('lpg', 'LPG'),
        ('electric', 'Electrico'),
        ('hybrid', 'Hibrido')
    ], 'Tipo de combustible', related="vehicle_id.fuel_type")
    license_plate = fields.Char(track_visibility="onchange", string="Matricula", related="vehicle_id.license_plate")
    model_id = fields.Many2one('fleet.vehicle.model', 'Modelo',
        track_visibility="onchange", required=True, related="vehicle_id.model_id" )
    nro_orden = fields.Char('Nro de orden', track_visibility='onchange', default="Borrador")
    raspn = fields.Char('R.A.S.P.N°', related="vehicle_id.raspn")
    area_asignada = fields.Char('Area asignada', track_visibility='onchange')
    fecha_inicio = fields.Date(string="Fecha inicio", required=True, track_visibility='onchange')
    fecha_fin = fields.Date(string="Fecha fin", required=False, track_visibility='onchange')
    hora_inicio = fields.Float(string="Hora inicio", track_visibility='onchange')
    hora_fin = fields.Float(string="Hora Fin", track_visibility='onchange')
    km_salida = fields.Integer(string='Km de salida', track_visibility='onchange')
    km_vuelta = fields.Integer(string='Km de vuelta', track_visibility='onchange')
    km_estimado_recorrido = fields.Float(string='Km estimado de recorrido', track_visibility='onchange')
    km_real_recorrido= fields.Float(string='Km real de recorrido', track_visibility='onchange')
    consumo_estimado = fields.Float(string='Consumo estimado x 100km L', track_visibility='onchange')
    date = fields.Date(
        string='Fecha', default=date.today(), required=True, track_visibility='onchange')

    fuel_logs_count = fields.Integer(compute="_compute_count_fuel", string='Combustible')

    def _compute_count_fuel(self):
        LogFuel = self.env['fleet.vehicle.log.fuel']
        for record in self:
            record.fuel_logs_count = LogFuel.search_count([('wo_vehicle_id', '=', record.id)])

    def action_see_log_fuel(self):
        self.ensure_one()
        return {
            'name': _('Registros de combustible de los vehículos'),
            'res_model': 'fleet.vehicle.log.fuel',
            'type': 'ir.actions.act_window',
            'views': [(False, 'list'), (False, 'form')],
            'view_mode': 'list, form',
            'context': {
                # "search_default_folder_id": self.documents_folder_id.id,
                "default_wo_vehicle_id": self.id,
                "default_vehicle_id": self.vehicle_id.id,
                "default_driver_id": self.driver_id.id,
                "searchpanel_default_wo_vehicle_id": self.id
            },
        }


    def button_cerrar(self):
        for i in self:
            values_odometer ={
                'vehicle_id':self.vehicle_id.id,
                'date':fields.Date.today(),
                'driver_id':self.driver_id,
                'unit':'kilometers',
                'value': self.vehicle_id.odometer+self.km_real_recorrido,
                'wo_vehicle_id':self.id
            }
            odometro = self.env['fleet.vehicle.odometer'].create(values_odometer)
            i.write({'state': 'closed'})