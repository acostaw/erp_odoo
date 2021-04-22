# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class cuentas_cobrar_pagar_community(models.Model):
#     _name = 'cuentas_cobrar_pagar_community.cuentas_cobrar_pagar_community'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100