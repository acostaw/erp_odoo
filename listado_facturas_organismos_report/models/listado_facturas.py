# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class ListadoFacturasOrganismosReportWizard(models.TransientModel):
    _name = 'listado_facturas_organismos.report.wizard'

    date_start = fields.Date(string="Fecha Inicio", required=True, default=fields.Date.today)
    date_end = fields.Date(string="Fecha Final", required=True, default=fields.Date.today)

    @api.multi
    def get_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_start': self.date_start,
                'date_end': self.date_end,
            },
        }

        return self.env.ref('listado_facturas_organismos_report.recap_report').report_action(self, data=data)


class ReportListadoFacturasOrganismos(models.AbstractModel):

    _name = 'report.listado_facturas_organismos_report.recap_report_view'

    @api.model
    def _get_report_values(self, docids, data=None):
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        date_start_obj = datetime.strptime(date_start, DATE_FORMAT)
        date_end_obj = datetime.strptime(date_end, DATE_FORMAT)


        start_report = date_start_obj.strftime('%d/%m/%Y')
        end_report = date_end_obj.strftime('%d/%m/%Y')

        facturas = self.env['account.invoice'].search(
            [('type', '=', 'out_invoice'), ('state', 'in', ['open', 'paid']),
             ('date_invoice', '>=', date_start),
             ('date_invoice', '<=', date_end)])


        docs = sorted(facturas, key = lambda x: x.fake_number)
        docs = sorted(docs, key=lambda x: x.date_invoice)
        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_start':start_report,
            'date_end': end_report,
            'docs': docs,
        }
