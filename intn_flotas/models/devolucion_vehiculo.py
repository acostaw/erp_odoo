# -*- coding: utf-8 -*-

from odoo import models, api, fields, exceptions


class DevolucionVehiculos(models.Model):
    _name = 'devolucion.vehiculo'
    _description = 'Devolución de vehiculos'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _rec_name='vehicle_id'

    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehiculo", required=True, track_visibility='onchange')

    date = fields.Date(string="Fecha", required=True, default=fields.Date.today, track_visibility='onchange')
    driver_id = fields.Many2one('res.partner', string="Conductor", related="vehicle_id.driver_id", required=True,
                                readonly=False, track_visibility=True)

    km_vehiculo = fields.Integer('Km Vehiculo', required=True, track_visibility=True)

    observacion = fields.Text('Observación', required=False, track_visibility='onchange')

    titulo_propiedad = fields.Selection(string='Titulo de propiedad', selection=[('si', 'Tiene'), ('no', 'No tiene')],
                                        default='si', track_visibility='onchange')
    certificado_mopc = fields.Selection(string='Certificado Inscripción M.O.P.C',
                                        selection=[('si', 'Tiene'), ('no', 'No tiene')], default='si',
                                        track_visibility='onchange')
    cobertura_seguro = fields.Selection(string='Cobertura de seguro', selection=[('si', 'Tiene'), ('no', 'No tiene')],
                                        default='si', track_visibility='onchange')

    tarjeta_identificatoria = fields.Selection(string='Tarjeta identificatoria',
                                               selection=[('m_bueno', 'M. Bueno'), ('bueno', 'Bueno'),
                                                          ('regural', 'Regular'), ('malo', 'Malo'),
                                                          ('no_tiene', 'No tiene')], default='bueno',
                                               track_visibility='onchange')
    logotipo_puertas = fields.Selection(string='Logotipo en puertas',
                                               selection=[('m_bueno', 'M. Bueno'), ('bueno', 'Bueno'),
                                                          ('regural', 'Regular'), ('malo', 'Malo'),
                                                          ('no_tiene', 'No tiene')], default='bueno',
                                               track_visibility='onchange')
    habilitacion = fields.Selection(string='Habilitación',
                                               selection=[('m_bueno', 'M. Bueno'), ('bueno', 'Bueno'),
                                                          ('regural', 'Regular'), ('malo', 'Malo'),
                                                          ('no_tiene', 'No tiene')], default='bueno',
                                               track_visibility='onchange')


    situacion_general_ids = fields.One2many('situacion.general.vehiculo','devolucion_id',string='Situacion general del vehiculo')

    @api.onchange('date')
    @api.depends('date')
    def onChangeFecha(self):
        self.update({'situacion_general_ids': [(5, 0, 0)]})
        lines = []
        tasks = []
        unique_task = []
        tasks_ids = self.env['situacion.general.items'].search([('sequence', '!=', False)])
        for task in tasks_ids:
            tasks.append(task.id)
        if tasks:
            unique_task = set(tasks)
        for curr_task in unique_task:
            d = {'item_id': curr_task, 'devolucion_id': self.id}
            lines.append((0, 0, d))
        self.update({'situacion_general_ids': lines})




class SituacionGeneralVehiculo(models.Model):
    _name = 'situacion.general.vehiculo'
    # _rec_name = "workorder_id"

    devolucion_id = fields.Many2one('devolucion.vehiculo', string='Devolucion de Vehiculos')
    item_id = fields.Many2one("situacion.general.items", string='Item', readonly=False)
    m_bueno = fields.Boolean('Muy bueno', default=False)
    bueno = fields.Boolean('Bueno', default=False)
    regular = fields.Boolean('Regular', default=False)
    malo = fields.Boolean('Malo', default=False)
    no_tiene = fields.Boolean('No tiene', default=False)


class SituacionGeneralItems(models.Model):
    _name = 'situacion.general.items'

    name = fields.Char(string='Descripcion', required=True)
    active = fields.Boolean(default=True, string="Activo")
    sequence = fields.Integer('Secuencia')
