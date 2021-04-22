# -*- coding: utf-8 -*-

from odoo import models, fields, api
import xlsxwriter, base64


class WizardReporteCompra(models.TransientModel):
    _name = 'reporte_compraventa.wizardcompra'

    fecha_inicio = fields.Date(string='Fecha Inicio', required=True)
    fecha_fin = fields.Date(string='Fecha Fin', required=True)
    

    def print_report(self):
        datas = {
            'fecha_inicio': self.fecha_inicio,
            'fecha_fin': self.fecha_fin,
            
        }

        return self.env.ref('reporte_compraventa.account_invoices_compras_action').report_action(self, data=datas)

    def print_report_xlsx(self):
        return self.env.ref('reporte_compraventa.reporte_compra_xlsx_action').report_action(self)


class ReporteComprasXLSX(models.AbstractModel):
    _name = 'report.reporte_compraventa.reporte_compra_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, datas):
        
        facturas = self.env['account.invoice'].search(
            [('type', '=', 'in_invoice'), ('state', 'in', ['open', 'paid']),
                ('date_invoice', '>=', datas.fecha_inicio),
                ('date_invoice', '<=', datas.fecha_fin),('tax_line_ids','!=',False)])
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

        simpleWrite("Razon social:", bold)
        rightAndWrite(self.env.user.company_id.name)
        breakAndWrite("RUC:", bold)
        rightAndWrite(self.env.user.company_id.partner_id.vat)
        breakAndWrite("Periodo:", bold)
        rightAndWrite("Del " +datas.fecha_inicio.strftime("%d/%m/%Y") + " al " + datas.fecha_fin.strftime('%d/%m/%Y'))
        addSalto()
        addRight()
        addRight()
        addRight()
        addRight()
        simpleWrite('Libro de compras - Ley 125/91', bold)
        breakAndWrite("Nro", bold)
        rightAndWrite("Fecha", bold)
        rightAndWrite("Proveedor", bold)

        rightAndWrite("RUC del Proveedor", wrapped_text_bold)

        rightAndWrite("Tipo doc.", bold)
        rightAndWrite("Nro. doc.", bold)
        rightAndWrite("Importe total facturado con IVA incluido", wrapped_text_bold)
        rightAndWrite("Importe sin IVA 10%", wrapped_text_bold)
        rightAndWrite("Debito fiscal 10%", wrapped_text_bold)
        rightAndWrite("Importe sin IVA 5%", wrapped_text_bold)
        rightAndWrite("Debito fiscal 5%", wrapped_text_bold)
        rightAndWrite("Importes exentos", wrapped_text_bold)
        
        cont = 0
        total_gral_total = 0
        total_gral_base10 = 0
        total_gral_base5 = 0
        total_gral_iva10 = 0
        total_gral_iva5 = 0
        total_gral_exentas = 0
        for i in facturas.sorted(key=lambda r: r.date_invoice):
            a = 1
            cont += 1
            total_factura = i.amount_total_company_signed
            base10 = 0
            base5 = 0
            exentas = 0
            iva10 = 0
            iva5 = 0
            for t in i.tax_line_ids:
                if t.tax_id.amount==10:
                    base10=t.base
                    iva10=t.amount_total
                if t.tax_id.amount==5:
                    base5=t.base
                    iva5=t.amount_total
                if t.tax_id.amount==0:
                    exentas=t.base
            total_gral_total += total_factura
            total_gral_base10 += base10
            total_gral_base5 += base5
            total_gral_iva10 += iva10
            total_gral_iva5 += iva5
            total_gral_exentas += exentas

            breakAndWrite(cont)
            rightAndWrite(i.date_invoice.strftime("%d/%m/%Y"))
            rightAndWrite(i.partner_id.name)
            rightAndWrite(i.partner_id.vat)

            if i.date_invoice < i.date_due:
                rightAndWrite("Credito")
            else:
                rightAndWrite("Contado")
            rightAndWrite(i.reference)
            rightAndWrite(total_factura, numerico)
            rightAndWrite(base10, numerico)
            rightAndWrite(iva10, numerico)
            rightAndWrite(base5, numerico)
            rightAndWrite(iva5, numerico)
            rightAndWrite(exentas, numerico)
            
        addSalto()
        addRight()
        addRight()
        addRight()
        addRight()
        addRight()
        rightAndWrite(total_gral_total, numerico_total)
        rightAndWrite(total_gral_base10, numerico_total)
        rightAndWrite(total_gral_iva10, numerico_total)
        rightAndWrite(total_gral_base5, numerico_total)
        rightAndWrite(total_gral_iva5, numerico_total)
        rightAndWrite(total_gral_exentas, numerico_total)

        notas = self.env['account.invoice'].search(
            [('type', '=', 'out_refund'), ('state', 'in', ['open', 'paid','cancel']),
                ('date_invoice', '>=', datas.fecha_inicio),
                ('date_invoice', '<=', datas.fecha_fin),('tax_line_ids','!=',False)])
        
        breakAndWrite('Notas de crédito emitidas', bold)
        breakAndWrite("Nro", bold)
        rightAndWrite("Fecha", bold)
        rightAndWrite("Cliente", bold)
        rightAndWrite("RUC o CI del Cliente", wrapped_text_bold)
        rightAndWrite("Tipo doc.", bold)
        rightAndWrite("Nro. doc.", bold)
        rightAndWrite("Importe total con IVA incluido", wrapped_text_bold)
        rightAndWrite("Importe sin IVA 10%", wrapped_text_bold)
        rightAndWrite("Debito fiscal 10%", wrapped_text_bold)
        rightAndWrite("Importe sin IVA 5%", wrapped_text_bold)
        rightAndWrite("Debito fiscal 5%", wrapped_text_bold)
        rightAndWrite("Importes exentos", wrapped_text_bold)

        cont = 0
        total_gral_total = 0
        total_gral_base10 = 0
        total_gral_base5 = 0
        total_gral_iva10 = 0
        total_gral_iva5 = 0
        total_gral_exentas = 0
        for i in notas.sorted(key=lambda x: x.number):
            cont += 1
            if i.state!='cancel':
                total_factura = i.amount_total_company_signed*-1
            else:
                total_factura=0
            base10 = 0
            base5 = 0
            exentas = 0
            iva10 = 0
            iva5 = 0
            for t in i.tax_line_ids:
                if t.tax_id.amount==10:
                    base10=t.base
                    iva10=t.amount_total
                if t.tax_id.amount==5:
                    base5=t.base
                    iva5=t.amount_total
                if t.tax_id.amount==0:
                    exentas=t.base
            total_gral_total += total_factura
            total_gral_base10 += base10
            total_gral_base5 += base5
            total_gral_iva10 += iva10
            total_gral_iva5 += iva5
            total_gral_exentas += exentas

            breakAndWrite(cont)
            if i.state != 'cancel':
                rightAndWrite(i.date_invoice.strftime("%d/%m/%Y"))
            else:
                rightAndWrite("")
            if i.state != 'cancel':
                rightAndWrite(i.partner_id.name)
            else:
                rightAndWrite("Anulado")
            if i.state != 'cancel':
                rightAndWrite(i.partner_id.vat)
            else:
                rightAndWrite("")

            if i.state != 'cancel':
                
                rightAndWrite("Nota de crédito")
            else:
                rightAndWrite("")
            rightAndWrite(i.reference)
            if i.state != 'cancel':
                rightAndWrite(total_factura, numerico)
            else:
                rightAndWrite(0)
            if i.state != 'cancel':
                rightAndWrite(base10, numerico)
            else:
                rightAndWrite(0)
            if i.state != 'cancel':
                rightAndWrite(iva10, numerico)
            else:
                rightAndWrite(0)
            if i.state != 'cancel':
                rightAndWrite(base5, numerico)
            else:
                rightAndWrite(0)
            if i.state != 'cancel':
                rightAndWrite(iva5, numerico)
            else:
                rightAndWrite(0)
            if i.state != 'cancel':
                rightAndWrite(exentas, numerico)
            else:
                rightAndWrite(0)
           
        addSalto()
        addRight()
        addRight()
        addRight()
        addRight()
        addRight()
        rightAndWrite(total_gral_total, numerico_total)
        rightAndWrite(total_gral_base10, numerico_total)
        rightAndWrite(total_gral_iva10, numerico_total)
        rightAndWrite(total_gral_base5, numerico_total)
        rightAndWrite(total_gral_iva5, numerico_total)
        rightAndWrite(total_gral_exentas, numerico_total)




class WizardReporteVenta(models.TransientModel):
    _name = 'reporte_compraventa.wizardventa'

    fecha_inicio = fields.Date(string='Fecha Inicio', required=True)
    fecha_fin = fields.Date(string='Fecha Fin', required=True)

    def print_report(self):
        datas = {
            'fecha_inicio': self.fecha_inicio,
            'fecha_fin': self.fecha_fin,
            
        }

        return self.env.ref('reporte_compraventa.account_invoices_ventas_action').report_action(self, data=datas)

    def print_report_xlsx(self):
        return self.env.ref('reporte_compraventa.reporte_venta_xlsx_action').report_action(self)




class ReporteVentasXLSX(models.AbstractModel):
    _name = 'report.reporte_compraventa.reporte_venta_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, datas):
       
        facturas = self.env['account.invoice'].search(
            [('type', '=', 'out_invoice'), ('state', 'in', ['open', 'paid', 'cancel']),
                ('date_invoice', '>=', datas.fecha_inicio),
                ('date_invoice', '<=', datas.fecha_fin),('tax_line_ids','!=',False)])
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

        simpleWrite("Razon social:", bold)
        rightAndWrite(self.env.user.company_id.name)
        breakAndWrite("RUC:", bold)
        rightAndWrite(self.env.user.company_id.partner_id.vat)
        breakAndWrite("Periodo:", bold)
        rightAndWrite("Del " +datas.fecha_inicio.strftime("%d/%m/%Y") + " al " + datas.fecha_fin.strftime('%d/%m/%Y'))
        addSalto()
        addRight()
        addRight()
        addRight()
        addRight()
        simpleWrite('Libro de ventas - Ley 125/91', bold)
        breakAndWrite("Nro", bold)
        rightAndWrite("Fecha", bold)
        rightAndWrite("Cliente", bold)
        rightAndWrite("RUC o CI del Cliente", wrapped_text_bold)
        rightAndWrite("Tipo doc.", bold)
        rightAndWrite("Nro. doc.", bold)
        rightAndWrite("Importe total facturado con IVA incluido", wrapped_text_bold)
        rightAndWrite("Importe sin IVA 10%", wrapped_text_bold)
        rightAndWrite("Debito fiscal 10%", wrapped_text_bold)
        rightAndWrite("Importe sin IVA 5%", wrapped_text_bold)
        rightAndWrite("Debito fiscal 5%", wrapped_text_bold)
        rightAndWrite("Importes exentos", wrapped_text_bold)
        

        cont = 0
        total_gral_total = 0
        total_gral_base10 = 0
        total_gral_base5 = 0
        total_gral_iva10 = 0
        total_gral_iva5 = 0
        total_gral_exentas = 0
        for i in facturas.sorted(key=lambda x: x.fake_number):
            cont += 1
            if i.state!='cancel':
                total_factura = i.amount_total_company_signed
            else:
                total_factura=0
            base10 = 0
            base5 = 0
            exentas = 0
            iva10 = 0
            iva5 = 0
            for t in i.tax_line_ids:
                if t.tax_id.amount==10:
                    base10=t.base
                    iva10=t.amount_total
                if t.tax_id.amount==5:
                    base5=t.base
                    iva5=t.amount_total
                if t.tax_id.amount==0:
                    exentas=t.base
            total_gral_total += total_factura
            total_gral_base10 += base10
            total_gral_base5 += base5
            total_gral_iva10 += iva10
            total_gral_iva5 += iva5
            total_gral_exentas += exentas

            breakAndWrite(cont)
            if i.state != 'cancel':
                rightAndWrite(i.date_invoice.strftime("%d/%m/%Y"))
            else:
                rightAndWrite("")
            if i.state != 'cancel':
                rightAndWrite(i.partner_id.name)
            else:
                rightAndWrite("Anulado")
            if i.state != 'cancel':
                rightAndWrite(i.partner_id.vat)
            else:
                rightAndWrite("")

            if i.state != 'cancel':
                if i.date_invoice < i.date_due:
                    rightAndWrite("Credito")
                else:
                    rightAndWrite("Contado")
            else:
                rightAndWrite("")
            rightAndWrite(i.fake_number)
            if i.state != 'cancel':
                rightAndWrite(total_factura, numerico)
            else:
                rightAndWrite(0)
            if i.state != 'cancel':
                rightAndWrite(base10, numerico)
            else:
                rightAndWrite(0)
            if i.state != 'cancel':
                rightAndWrite(iva10, numerico)
            else:
                rightAndWrite(0)
            if i.state != 'cancel':
                rightAndWrite(base5, numerico)
            else:
                rightAndWrite(0)
            if i.state != 'cancel':
                rightAndWrite(iva5, numerico)
            else:
                rightAndWrite(0)
            if i.state != 'cancel':
                rightAndWrite(exentas, numerico)
            else:
                rightAndWrite(0)
           
        addSalto()
        addRight()
        addRight()
        addRight()
        addRight()
        addRight()
        rightAndWrite(total_gral_total, numerico_total)
        rightAndWrite(total_gral_base10, numerico_total)
        rightAndWrite(total_gral_iva10, numerico_total)
        rightAndWrite(total_gral_base5, numerico_total)
        rightAndWrite(total_gral_iva5, numerico_total)
        rightAndWrite(total_gral_exentas, numerico_total)

        notas = self.env['account.invoice'].search(
            [('type', '=', 'in_refund'), ('state', 'in', ['open', 'paid']),
                ('date_invoice', '>=', datas.fecha_inicio),
                ('date_invoice', '<=', datas.fecha_fin),('tax_line_ids','!=',False)])
        
        breakAndWrite('Notas de crédito recibidas', bold)
        breakAndWrite("Nro", bold)
        rightAndWrite("Fecha", bold)
        rightAndWrite("Proveedor", bold)
        rightAndWrite("RUC o CI del Proveedor", wrapped_text_bold)
        rightAndWrite("Tipo doc.", bold)
        rightAndWrite("Nro. doc.", bold)
        rightAndWrite("Importe total con IVA incluido", wrapped_text_bold)
        rightAndWrite("Importe sin IVA 10%", wrapped_text_bold)
        rightAndWrite("Debito fiscal 10%", wrapped_text_bold)
        rightAndWrite("Importe sin IVA 5%", wrapped_text_bold)
        rightAndWrite("Debito fiscal 5%", wrapped_text_bold)
        rightAndWrite("Importes exentos", wrapped_text_bold)

        cont = 0
        total_gral_total = 0
        total_gral_base10 = 0
        total_gral_base5 = 0
        total_gral_iva10 = 0
        total_gral_iva5 = 0
        total_gral_exentas = 0
        for i in notas.sorted(key=lambda x: x.date_invoice):
            cont += 1
            if i.state!='cancel':
                total_factura = i.amount_total_company_signed*-1
            else:
                total_factura=0
            base10 = 0
            base5 = 0
            exentas = 0
            iva10 = 0
            iva5 = 0
            for t in i.tax_line_ids:
                if t.tax_id.amount==10:
                    base10=t.base
                    iva10=t.amount_total
                if t.tax_id.amount==5:
                    base5=t.base
                    iva5=t.amount_total
                if t.tax_id.amount==0:
                    exentas=t.base
            total_gral_total += total_factura
            total_gral_base10 += base10
            total_gral_base5 += base5
            total_gral_iva10 += iva10
            total_gral_iva5 += iva5
            total_gral_exentas += exentas

            breakAndWrite(cont)
            if i.state != 'cancel':
                rightAndWrite(i.date_invoice.strftime("%d/%m/%Y"))
            else:
                rightAndWrite("")
            if i.state != 'cancel':
                rightAndWrite(i.partner_id.name)
            else:
                rightAndWrite("Anulado")
            if i.state != 'cancel':
                rightAndWrite(i.partner_id.vat)
            else:
                rightAndWrite("")

            if i.state != 'cancel':
                
                rightAndWrite("Nota de crédito")
            else:
                rightAndWrite("")
            rightAndWrite(i.reference)
            if i.state != 'cancel':
                rightAndWrite(total_factura, numerico)
            else:
                rightAndWrite(0)
            if i.state != 'cancel':
                rightAndWrite(base10, numerico)
            else:
                rightAndWrite(0)
            if i.state != 'cancel':
                rightAndWrite(iva10, numerico)
            else:
                rightAndWrite(0)
            if i.state != 'cancel':
                rightAndWrite(base5, numerico)
            else:
                rightAndWrite(0)
            if i.state != 'cancel':
                rightAndWrite(iva5, numerico)
            else:
                rightAndWrite(0)
            if i.state != 'cancel':
                rightAndWrite(exentas, numerico)
            else:
                rightAndWrite(0)
           
        addSalto()
        addRight()
        addRight()
        addRight()
        addRight()
        addRight()
        rightAndWrite(total_gral_total, numerico_total)
        rightAndWrite(total_gral_base10, numerico_total)
        rightAndWrite(total_gral_iva10, numerico_total)
        rightAndWrite(total_gral_base5, numerico_total)
        rightAndWrite(total_gral_iva5, numerico_total)
        rightAndWrite(total_gral_exentas, numerico_total)



