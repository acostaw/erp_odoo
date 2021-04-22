# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class ServiciosDepartamentoReportWizard(models.TransientModel):
    _name = 'listado_servicios_departamento.report.wizard'

    date_start = fields.Date(string="Fecha Inicio", null=True,required=True)
    date_end = fields.Date(string="Fecha Final", null=True,required=True)

    # mes = fields.Selection(string="Mes", selection=[('enero', 'Enero'), ('fecbrero', 'Febrero'),
    #                                                 ('marzo', 'Marzo'), (
    #                                                     'abril', 'Abril'),
    #                                                 ('mayo', 'Mayo'),
    #                                                 ('junio', 'Junio'),
    #                                                 ('julio', 'Julio'),
    #                                                 ('agosto', 'Agosto')
    #                                                 ('septiembre', 'Septiembre'), ('octubre', 'Octubre'),
    #                                                 ('noviembre', 'Noviembre'), ('diciembre', 'Diciembre')],
    #                        required=True)

    organismo_id = fields.Many2one('intn.organismos', string="Organismo",required=True)

    @api.multi
    def get_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_start': self.date_start,
                'date_end': self.date_end,
                'organismo_id': self.organismo_id.id,
            },
        }

        return self.env.ref('listado_servicios_departamento_report.recap_report').report_action(self, data=data)


class ReportServiciosDepartamento(models.AbstractModel):

    _name = 'report.listado_servicios_departamento_report.recap_report_view'

    @api.model
    def _get_report_values(self, docids, data=None):
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        date_start_obj = datetime.strptime(date_start, DATE_FORMAT)
        date_end_obj = datetime.strptime(date_end, DATE_FORMAT)

        organismo_id = data['form']['organismo_id']

        start_report = date_start_obj.strftime('%d/%m/%Y')
        end_report = date_end_obj.strftime('%d/%m/%Y')

        facturas = self.env['account.invoice'].search(
            [('type', '=', 'out_invoice'), ('state', 'in', ['open', 'paid']),
             ('date_invoice', '>=', date_start),
             ('date_invoice', '<=', date_end)])

        docs = []

        organismo = self.env['intn.organismos'].search([('id','=', organismo_id)])

        for factura in facturas:
            departamento = ''
            cantidad = 0
            for line in factura.invoice_line_ids:
                if line.product_id.organismo_id.id == organismo_id:
                    if factura.partner_id.state_id:
                        departamento = factura.partner_id.state_id.name
                    else:
                        departamento = 'Indefinido'
                    cantidad = line.quantity
                    docs.append({
                        'departamento': departamento,
                        'cantidad': cantidad
                    })

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_start': start_report,
            'date_end': end_report,
            'docs': docs,
            'organismo':organismo
        }
