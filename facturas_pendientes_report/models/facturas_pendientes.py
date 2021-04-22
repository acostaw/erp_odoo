# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class FacturasPendientesReportWizard(models.TransientModel):
    _name = 'facturas_pendientes.report.wizard'

    date_start = fields.Date(string="Fecha Inicio", null=True)
    date_end = fields.Date(string="Fecha Final", null=True)
    partner_id = fields.Many2one('res.partner', string="Cliente")

    @api.multi
    def get_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_start': self.date_start,
                'date_end': self.date_end,
                'partner_id': self.partner_id.id,
            },
        }

        return self.env.ref('facturas_pendientes_report.recap_report').report_action(self, data=data)


class ReportFacturasPendientes(models.AbstractModel):

    _name = 'report.facturas_pendientes_report.recap_report_view'

    @api.model
    def _get_report_values(self, docids, data=None):
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        start_report=''
        end_report=''
        if date_start:
            date_start_obj = datetime.strptime(date_start, DATE_FORMAT)
            start_report = date_start_obj.strftime('%d/%m/%Y')
        if date_end:
            date_end_obj = datetime.strptime(date_end, DATE_FORMAT)
            end_report = date_end_obj.strftime('%d/%m/%Y')
        partner_id = data['form']['partner_id']

        # print(partner_id)

        if partner_id:
            if date_start and date_end:
                facturas = self.env['account.invoice'].search(
                    [('type', '=', 'out_invoice'), ('state', 'in', ['open', 'in_payment']),
                     ('date_invoice', '>=', date_start_obj.strftime(DATETIME_FORMAT)),
                     ('date_invoice', '<=', date_end_obj.strftime(DATETIME_FORMAT)),
                     ('tax_line_ids', '!=', False)]).filtered(lambda x: x.partner_id.id == partner_id or x.partner_id.parent_id.id == partner_id)
            else:
                facturas = self.env['account.invoice'].search(
                    [('type', '=', 'out_invoice'), ('state', 'in', ['open', 'in_payment']),
                     ('tax_line_ids', '!=', False)]).filtered(lambda x: x.partner_id.id == partner_id or x.partner_id.parent_id.id == partner_id)
        else:
            if date_start and date_end:
                facturas = self.env['account.invoice'].search(
                    [('type', '=', 'out_invoice'), ('state', 'in', ['open', 'in_payment']),
                     ('date_invoice', '>=', date_start_obj.strftime(DATETIME_FORMAT)),
                     ('date_invoice', '<=', date_end_obj.strftime(DATETIME_FORMAT)),
                     ('tax_line_ids', '!=', False)])
            else:
                facturas = self.env['account.invoice'].search(
                    [('type', '=', 'out_invoice'), ('state', 'in', ['open', 'in_payment']),
                     ('tax_line_ids', '!=', False)])

        docs = sorted(facturas, key = lambda x: x.date_invoice)

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_start':start_report,
            'date_end': end_report,
            'partner_id': partner_id,
            'docs': docs,
        }
