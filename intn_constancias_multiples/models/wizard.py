# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
import operator


class TipoConstanciasWizard(models.TransientModel):
    _name = 'tipo.constancias.wizard'

    tipo_constancia_id = fields.Many2one('tipo.constancias',string="Tipo de Constancia", required=True)
    order_id = fields.Many2one('sale.order',string="Expediente", required=True)

    @api.multi
    def get_constancia(self):
        view = self.env.ref('intn_constancias_multiples.constancias_multiples_form_view')
        
        return {
            'name': 'Constancias',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'constancias.multiples',
            'context': {'default_tipo_constancia_id': self.tipo_constancia_id.id,'default_order_id':self.order_id.id},
            'view_id': view.id,
            'target': '_blank',
        }
