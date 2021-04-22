# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
import operator


class DetalleCobrosReportWizard(models.TransientModel):
    _name = 'detalle_cobros.report.wizard'

    date_start = fields.Date(string="Fecha Inicio", required=True, default=fields.Date.today)
    date_end = fields.Date(string="Fecha Final", required=True, default=fields.Date.today)
    aqui_pago = fields.Boolean(string="Reporte de Aqui Pago", default=False)
    partner_id = fields.Many2one('res.partner', string="Cliente")

    @api.multi
    def get_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_start': self.date_start,
                'date_end': self.date_end,
                'aqui_pago':self.aqui_pago,
                'partner_id': self.partner_id.id,
            },
        }

        return self.env.ref('detalle_cobros_report.recap_report').report_action(self, data=data)


class ReportDetalleCobros(models.AbstractModel):

    _name = 'report.detalle_cobros_report.recap_report_view'

    @api.model
    def _get_report_values(self, docids, data=None):
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        aqui_pago = data['form']['aqui_pago']
        date_start_obj = datetime.strptime(date_start, DATE_FORMAT)
        date_end_obj = datetime.strptime(date_end, DATE_FORMAT)
        partner_id = data['form']['partner_id']


        start_report = date_start_obj.strftime('%d/%m/%Y')
        end_report = date_end_obj.strftime('%d/%m/%Y')

        docs = []

        if partner_id:
            recibos = self.env['grupo_account_payment.payment.group'].search(
                [('state', 'in', ['done']),
                 ('fecha', '>=', date_start_obj.strftime(DATETIME_FORMAT)),
                 ('fecha', '<=', date_end_obj.strftime(DATETIME_FORMAT))]).filtered(
                    lambda x: x.partner_id.id == partner_id or x.partner_id.parent_id.id == partner_id)
        else:
            recibos = self.env['grupo_account_payment.payment.group'].search(
                [('state', 'in', ['done']),
                 ('fecha', '>=', date_start_obj.strftime(DATETIME_FORMAT)),
                 ('fecha', '<=', date_end_obj.strftime(DATETIME_FORMAT))])

        facturas_reporte = []

        for recibo in recibos:
            cheques=[]
            aquiPago = "1"

            for pago in recibo.payment_ids:
                cheques.append(pago.nro_cheque)
                if pago.tipo_pago == 'aquiPago':
                    aquiPago = True
                else:
                    aquiPago = False

            for pago in recibo.refund_ids:
                aquiPago = False

            if aqui_pago == aquiPago:
                for factura in recibo.paid_invoice_ids:
                    mora = False
                    ivaCinco = 0
                    ivaDiez = 0
                    factura_nro = self.env['account.invoice'].search([('fake_number', '=', factura.fake_number),('state','in',['open','paid'])], limit=1)

                    if factura.fake_number not in facturas_reporte:
                        facturas_reporte.append(factura.fake_number)

                        if factura.factura_origen_mora or factura.facturas_origen_mora:
                            mora = True
                        if factura.partner_id.parent_id:
                            cliente = factura.partner_id.parent_id.name
                        else:
                            cliente = factura.partner_id.name

                        for iva in factura.tax_line_ids:
                            if 'IVA 5' in iva.name:
                                ivaCinco += iva.amount
                            elif 'IVA 10' in iva.name:
                                ivaDiez += iva.amount

                        if factura.state != 'draft' and factura.state != 'cancel':

                            docs.append({
                                'factura': factura.fake_number,
                                'fecha_emision': factura.date_invoice,
                                'fecha_vencimiento': factura.date_due,
                                'cliente': cliente,
                                'total': factura.amount_total,
                                'fecha_cobro' : recibo.fecha,
                                'factura_mora':mora,
                                'cheque_nro': cheques,
                                'ivaCinco': ivaCinco,
                                'ivaDiez':ivaDiez
                            })

                        docs = sorted(docs, key = lambda x: x.get('factura'))
                        docs = sorted(docs, key=lambda x: x.get('fecha_cobro'))

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'aqui_pago': aqui_pago,
            'date_start': start_report,
            'date_end': end_report,
            'docs': docs,
        }
