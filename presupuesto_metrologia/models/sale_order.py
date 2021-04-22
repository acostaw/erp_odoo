# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import datetime,math,locale
from odoo.exceptions import ValidationError
class ReporteAbstract(models.AbstractModel):
    _name = 'report.presupuesto_metrologia.presupuesto_onm'


    @api.model
    def _get_report_values(self, docids, data=None):
        report_name = 'presupuesto_metrologia.presupuesto_onm'
        report = self.env['ir.actions.report']._get_report_from_name(report_name)
        return {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': self.env[report.model].browse(docids),
            'version_metrologia': self.env['ir.config_parameter'].sudo().get_param(
                    'version_metrologia_parameter')
        }


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _servicioAptitud(self):
        for this in self:
            aptitud= False
            for order_line in this.order_line:
                if order_line.filtered(lambda z:'Aptitud' in z.product_id.name ):
                    aptitud = True
            return aptitud