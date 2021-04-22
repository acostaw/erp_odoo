# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
import operator


class FacturaServicioReportWizard(models.TransientModel):
    _name = 'factura_servicios.report.wizard'

    date_start = fields.Date(string="Fecha Inicio", required=True, default=fields.Date.today)
    date_end = fields.Date(string="Fecha Final", required=True, default=fields.Date.today)
    aqui_pago = fields.Boolean(string="Reporte de Aqui Pago", default=False)
    partner_id = fields.Many2one('res.partner', string="Cliente")
    product_ids = fields.Many2many('product.product', string='Productos')

    @api.multi
    def get_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_start': self.date_start,
                'date_end': self.date_end,
                'aqui_pago': self.aqui_pago,
                'partner_id': self.partner_id.id,
                'product_ids': self.product_ids.ids,
            },
        }
        return self.env.ref('report_factura_por_servicio.factura_servicios_report_pdf').report_action(self, data=data)

    def get_report_xlsx(self):
        return self.env.ref('report_factura_por_servicio.factura_servicios_report_xlsx').report_action(self)


class ReportFacturaServicio(models.AbstractModel):
    _name = 'report.report_factura_por_servicio.factura_servicios_report_t'

    @api.model
    def _get_report_values(self, docids, data=None):
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        aqui_pago = data['form']['aqui_pago']
        date_start_obj = datetime.strptime(date_start, DATE_FORMAT)
        date_end_obj = datetime.strptime(date_end, DATE_FORMAT)
        partner_id = data['form']['partner_id']
        product_ids = data['form']['product_ids']

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
            cheques = []
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
                facturas = recibo.paid_invoice_ids
                if product_ids:
                    facturas = facturas.filtered(
                        lambda x: any(
                            [product_id in x.mapped('invoice_line_ids.product_id').ids for product_id in product_ids]))
                for factura in facturas:
                    mora = False
                    ivaCinco = 0
                    ivaDiez = 0
                    factura_nro = self.env['account.invoice'].search(
                        [('fake_number', '=', factura.fake_number), ('state', 'in', ['open', 'paid'])], limit=1)

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
                                'fecha_cobro': recibo.fecha,
                                'factura_mora': mora,
                                'cheque_nro': cheques,
                                'ivaCinco': ivaCinco,
                                'ivaDiez': ivaDiez,
                                'user_id': factura.user_id

                            })

                        docs = sorted(docs, key=lambda x: x.get('factura'))
                        docs = sorted(docs, key=lambda x: x.get('fecha_cobro'))

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'aqui_pago': aqui_pago,
            'date_start': start_report,
            'date_end': end_report,
            'docs': docs,
        }


class ReporteComprasXLSX(models.AbstractModel):
    _name = 'report.report_factura_por_servicio.factura_servicios_xlsx_t'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, datas):
        global sheet
        global bold
        global num_format
        global position_x
        global position_y
        sheet = workbook.add_worksheet('Hoja 1')
        bold = workbook.add_format({'bold': True})
        numerico = workbook.add_format({'num_format': True, 'align': 'right'})
        numerico.set_num_format('#,##0')
        numerico_total = workbook.add_format({'num_format': True, 'align': 'right', 'bold': True})
        numerico_total.set_num_format('#,##0')
        wrapped_text = workbook.add_format()
        wrapped_text.set_text_wrap()
        wrapped_text_bold = workbook.add_format({'bold': True})
        wrapped_text_bold.set_text_wrap()

        position_x = 0
        position_y = 0

        def addSalto():
            global position_x
            global position_y
            position_x = 0
            position_y += 1

        def addRight():
            global position_x
            position_x += 1

        def breakAndWrite(to_write, format=None):
            global sheet
            addSalto()
            sheet.write(position_y, position_x, to_write, format)

        def simpleWrite(to_write, format=None):
            global sheet
            sheet.write(position_y, position_x, to_write, format)

        def rightAndWrite(to_write, format=None):
            global sheet
            addRight()
            sheet.write(position_y, position_x, to_write, format)

        # date_start = data['form']['date_start']
        # date_end = data['form']['date_end']
        # aqui_pago = data['form']['aqui_pago']
        # date_start_obj = datetime.strptime(date_start, DATE_FORMAT)
        # date_end_obj = datetime.strptime(date_end, DATE_FORMAT)
        # partner_id = data['form']['partner_id']
        # product_ids = data['form']['product_ids']
        date_start = datas.date_start
        date_end = datas.date_end
        aqui_pago = datas.aqui_pago
        # date_start_obj = datetime.strptime(str(date_start), DATE_FORMAT)
        # date_end_obj = datetime.strptime(str(date_end), DATE_FORMAT)
        partner_id = datas.partner_id
        product_ids = datas.product_ids

        # start_report = date_start_obj.strftime('%d/%m/%Y')
        # end_report = date_end_obj.strftime('%d/%m/%Y')

        docs = []

        if partner_id:
            recibos = self.env['grupo_account_payment.payment.group'].search(
                [('state', 'in', ['done']),
                 ('fecha', '>=', date_start.strftime(DATETIME_FORMAT)),
                 ('fecha', '<=', date_end.strftime(DATETIME_FORMAT))]).filtered(
                lambda x: x.partner_id == partner_id or x.partner_id.parent_id == partner_id)
        else:
            recibos = self.env['grupo_account_payment.payment.group'].search(
                [('state', 'in', ['done']),
                 ('fecha', '>=', date_start.strftime(DATETIME_FORMAT)),
                 ('fecha', '<=', date_end.strftime(DATETIME_FORMAT))])

        facturas_reporte = []

        for recibo in recibos:
            cheques = []
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
                facturas = recibo.paid_invoice_ids
                if product_ids:
                    facturas = facturas.filtered(
                        lambda x: any(
                            [product_id in x.mapped('invoice_line_ids.product_id') for product_id in product_ids]))
                for factura in facturas:
                    mora = False
                    ivaCinco = 0
                    ivaDiez = 0
                    factura_nro = self.env['account.invoice'].search(
                        [('fake_number', '=', factura.fake_number), ('state', 'in', ['open', 'paid'])], limit=1)

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
                                'fecha_cobro': recibo.fecha,
                                'factura_mora': mora,
                                'cheque_nro': cheques,
                                'ivaCinco': ivaCinco,
                                'ivaDiez': ivaDiez,
                                'user_id': factura.user_id
                            })

                        docs = sorted(docs, key=lambda x: x.get('factura'))
                        docs = sorted(docs, key=lambda x: x.get('fecha_cobro'))

        simpleWrite('Facturas por Servicios', bold)
        addSalto()
        sheet.merge_range('A2:C2', 'Fecha Desde: ' + date_start.strftime('%d/%m/%Y'), bold)
        # breakAndWrite(, bold)
        sheet.merge_range('E2:G2', 'Fecha Desde: ' + date_end.strftime('%d/%m/%Y'), bold)
        # rightAndWrite('Fecha Hasta: ' + date_end.strftime('%d/%m/%Y'), bold)
        addSalto()
        addSalto()
        sheet.merge_range('A4:D4', 'Nro Factura', bold)
        # rightAndWrite('Nro de Factura', bold)
        sheet.merge_range('E4:J4', 'Montos Cobrados', bold)
        # rightAndWrite('Montos Cobrados', bold)
        sheet.merge_range('K4:L4', 'Fechas Facturas', bold)
        # rightAndWrite('Fechas Facturas', bold)
        breakAndWrite('Contado', bold)
        rightAndWrite('Crédito', bold)
        rightAndWrite('Interes', bold)
        rightAndWrite('Cliente', bold)
        rightAndWrite('Contado', bold)
        rightAndWrite('Crédito', bold)
        rightAndWrite('Interes', bold)
        rightAndWrite('IVA Exenta', bold)
        rightAndWrite('IVA 10%', bold)
        rightAndWrite('Cheque Nro', bold)
        rightAndWrite('Emisión', bold)
        rightAndWrite('Cobro', bold)
        rightAndWrite('Usuario Emisor', bold)
        for d in docs:
            breakAndWrite(
                d['factura'] if d['fecha_emision'] == d['fecha_vencimiento'] and not d['factura_mora'] else '')
            rightAndWrite(
                d['factura'] if d['fecha_emision'] != d['fecha_vencimiento'] and not d['factura_mora'] else '')
            rightAndWrite(d['factura'] if d['factura_mora'] else '')
            rightAndWrite(d['cliente'])
            rightAndWrite(d['total'] if d['fecha_emision'] == d['fecha_vencimiento'] and not d['factura_mora'] else '')
            rightAndWrite(d['total'] if d['fecha_emision'] != d['fecha_vencimiento'] and not d['factura_mora'] else '')
            rightAndWrite(d['total'] if d['factura_mora'] else '')
            addRight()
            rightAndWrite(d['ivaDiez'])
            rightAndWrite(' '.join([cheque if cheque else '' for cheque in d['cheque_nro']]))
            rightAndWrite(d['fecha_emision'].strftime('%d/%m/%Y'))
            rightAndWrite(d['fecha_cobro'].strftime('%d/%m/%Y'))
            rightAndWrite(d['user_id'].name)
        addSalto()
        addSalto()
        addRight()
        addRight()
        addRight()
        sheet.merge_range('A' + str(position_y + 1) + ':D' + str(position_y + 1), 'Totales', bold)
        total_contado = sum(
            [d['total'] if ['fecha_emision'] == d['fecha_vencimiento'] and not d['factura_mora'] else 0 for d in docs])
        rightAndWrite(total_contado, bold)
        total_credito = sum(
            [d['total'] if ['fecha_emision'] != d['fecha_vencimiento'] and not d['factura_mora'] else 0 for d in docs])
        rightAndWrite(total_credito, bold)
        total_mora = sum([d['total'] if d['factura_mora'] else 0 for d in docs])
        rightAndWrite(total_mora, bold)
        addRight()
        rightAndWrite(sum([d['ivaDiez'] for d in docs]), bold)
        addRight()
        rightAndWrite('Total', bold)
        rightAndWrite(total_contado + total_credito + total_mora, bold)
