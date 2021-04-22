# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class mrp_intn(models.Model):
#     _name = 'mrp_intn.mrp_intn'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100