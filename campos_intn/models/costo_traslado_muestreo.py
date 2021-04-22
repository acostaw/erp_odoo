# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CostoTrasladoMuestreo(models.Model):
    _name = 'intn.costo.traslado.muestreo'

    name = fields.Char(string="Ciudad/Departamento")
    monto = fields.Integer(string='Monto')