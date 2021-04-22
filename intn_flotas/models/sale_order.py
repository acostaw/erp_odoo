# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import models, fields, api, exceptions,_


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    wo_vehicle_count = fields.Integer('OT Count', compute='_compute_wo_vehicle_count')

    def _compute_wo_vehicle_count(self):
        wo_vehicle = self.env['workorder.vehicle'].search([('order_id', '=', self.id)])
        wo_vehicle_count_dict = len(wo_vehicle)
        for record in self:
            record.wo_vehicle_count = wo_vehicle_count_dict

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
                "default_order_id": self.id,
                "searchpanel_default_order_id": self.id
            },
        }