# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions,_

class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'


    nro_movil = fields.Integer('Nro de móvil', track_visibility='onchange')


    nro_registro = fields.Char('N° de registro', track_visibility='onchange')

    chasis = fields.Char('N° de chasis', track_visibility='onchange')

    raspn = fields.Char('RASPN', track_visibility='onchange')

    capacidad_tanque = fields.Integer('Capacidad del tanque (lts)', track_visibility='onchange')

    consumo_promedio = fields.Integer('Consumo promedio (lts/km)', track_visibility='onchange')

    polizas_ids = fields.One2many('polizas.vehicle', 'vehicle_id',
                                        string="Pólizas")

    desperfecto_mecanico_grave_ids = fields.One2many('desperfecto.mecanico.grave', 'vehicle_id',
                                        string="Desperfectos mecánicos graves")

    desperfecto_mecanico_grave = fields.Boolean('Desperfecto mecánico grave', store=True)

    disponibilidad = fields.Selection(string='Disponibilidad', selection=[(
             'disponible', 'Disponible'), ('no_disponible', 'No disponible')], default='disponible',
                                  track_visibility='onchange')

    fecha_disponibilidad = fields.Date('Fecha de disponibilidad', track_visibility='onchange' )

    last_workorder_date = fields.Date('Último viaje', compute="computeLastWorkorder")
    last_workorder_driver_id = fields.Many2one('res.partner', string="Último conductor", compute="computeLastWorkorder")
    next_service_date = fields.Date(string='Fecha del próximo servicio', track_visibility='onchange', compute="computeProximoMantenimiento")

    color_id = fields.Many2one('color.vehicle',string='Color')

    wo_vehicle_count = fields.Integer(compute="_compute_count_all_per", string='Orden de trabajo')
    devolucion_vehiculo_count = fields.Integer(compute="_compute_count_all_per", string='Devolucion Vehiculo')
    pipa_count = fields.Integer(compute="_compute_count_all_per", string='Informe averia')

    def _compute_count_all(self):
        WorkorderVehicle = self.env['workorder.vehicle']
        DevolucionVehiculo = self.env['devolucion.vehiculo']
        Pipa = self.env['informe.provisional.averia']
        for record in self:
            record.wo_vehicle_count = WorkorderVehicle.search_count([('vehicle_id', '=', record.id)])
            record.devolucion_vehiculo_count = DevolucionVehiculo.search_count([('vehicle_id', '=', record.id)])
            record.pipa_count = Pipa.search_count([('vehicle_id', '=', record.id)])

    def action_see_wo_vehicle(self):
        self.ensure_one()
        return {
            'name': _('Orden de Trabajo de Vehiculo'),
            'res_model': 'workorder.vehicle',
            'type': 'ir.actions.act_window',
            'views': [(False, 'list'), (False, 'form')],
            'view_mode': 'list, form',
            'context': {
                # "search_default_folder_id": self.documents_folder_id.id,
                "default_vehicle_id": self.id,
                "searchpanel_default_vehicle_id": self.id
            },
        }

    def action_see_devolucion_vehiculo(self):
        self.ensure_one()
        return {
            'name': _('Devolución de vehiculo'),
            'res_model': 'devolucion.vehiculo',
            'type': 'ir.actions.act_window',
            'views': [(False, 'list'), (False, 'form')],
            'view_mode': 'list, form',
            'context': {
                # "search_default_folder_id": self.documents_folder_id.id,
                "default_vehicle_id": self.id,
                "searchpanel_default_vehicle_id": self.id
            },
        }

    def action_see_pipa(self):
        self.ensure_one()
        return {
            'name': _('Informe Provisional de Avería en institucional (P.I.P.A.)'),
            'res_model': 'informe.provisional.averia',
            'type': 'ir.actions.act_window',
            'views': [(False, 'list'), (False, 'form')],
            'view_mode': 'list, form',
            'context': {
                # "search_default_folder_id": self.documents_folder_id.id,
                "default_vehicle_id": self.id,
                "searchpanel_default_vehicle_id": self.id
            },
        }


    _sql_constraints = [
        ('nro_movil_uniq', 'unique (nro_movil)',
         'El N° de móvil no puede repetirse !'),
    ]

    @api.onchange('desperfecto_mecanico_grave_ids')
    @api.depends('desperfecto_mecanico_grave_ids')
    def computeDMG(self):
        for this in self:
            flag = False
            if this.desperfecto_mecanico_grave_ids:
                for dmg in this.desperfecto_mecanico_grave_ids:
                    if dmg.fecha_inicio and not dmg.fecha_fin:
                        flag = True
            this.desperfecto_mecanico_grave = flag

    @api.onchange('disponibilidad')
    @api.depends('disponibilidad')
    def computeDisponibilidad(self):
        for this in self:
            if this.disponibilidad:
                if this.disponibilidad == 'no_disponible':
                    this.fecha_disponibilidad = False

    #@api.onchange('log_services')
    #@api.depends('log_services')
    def computeProximoMantenimiento(self):
        for this in self:
            if this.log_services:
                last_log = self.env['fleet.vehicle.log.services'].search(
                    [('vehicle_id', '=', this.id)],
                    order='next_service_date desc',
                    limit=1
                )
                this.next_service_date = last_log.next_service_date
            else:
                this.next_service_date = False


    def computeLastWorkorder(self):
        for this in self:
            last_wo = self.env['workorder.vehicle'].search(
                [('vehicle_id', '=', this.id)],
                order='date desc',
                limit=1
            )
            if last_wo:
                this.last_workorder_date = last_wo.date
                this.last_workorder_driver_id = last_wo.driver_id

class PolizasVehicle(models.Model):
    _name = 'polizas.vehicle'
    # _rec_name = "workorder_id"

    name= fields.Char('N° de póliza', required=True)
    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehiculo", required=True)
    partner_id = fields.Many2one('res.partner', string="Aseguradora")
    fecha_vencimiento = fields.Date(string="Fecha de Vencimiento", required=True)

class DesperfectoMecanicoGrave(models.Model):
    _name = 'desperfecto.mecanico.grave'
    # _rec_name = "workorder_id"

    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehiculo", required=True)
    name = fields.Char('Descripción', required=True)
    fecha_inicio = fields.Date(string="Fecha inicio", required=True)
    fecha_fin = fields.Date(string="Fecha fin", required=False)



class ColorVehicle(models.Model):
    _name = 'color.vehicle'
    # _rec_name = "workorder_id"

    name= fields.Char('Color', required=True)
