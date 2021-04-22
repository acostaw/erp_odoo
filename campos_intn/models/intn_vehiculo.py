# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class intnVehiculo(models.Model):
    _name = 'intn.vehiculo'

    name = fields.Char('Nombre', required=True)
    consumo_con_carga = fields.Integer('Consumo con carga', required=True)
    consumo_sin_carga = fields.Integer('Consumo sin carga', required=True)
