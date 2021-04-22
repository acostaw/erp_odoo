# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import datetime,math,locale
from odoo.exceptions import ValidationError


class accountInvoice(models.Model):
    _inherit = 'account.invoice'

    descripcion_detalle = fields.Char(default=" Factura según expediente N° ",readonly=True)

    limite_excedido = fields.Boolean(string="Limite Excedido", compute="get_lineas", default=False)

    barcode = fields.Char(compute='_barcode')

    comisionIVA = fields.Integer(compute='_comisionIVA')

    fecha_letras = fields.Char(compute='_fechaLetras')

    #locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8')

    cantidadImpresiones=fields.Integer(default=0,copy=False)

    detalle_pago = fields.Char(string="Descripción del Pago")

    monto_pago = fields.Monetary(string="Monto")

    descuento = fields.Integer(string="Descuento (%)")

    monto_descuento = fields.Integer(string="monto_descuento", compute="montoDescuento")

    por_descuento = fields.Char(string="Descuento (%)", compute="montoDescuento")



    def montoDescuento(self):
        for this in self:
            producto_de_descuento = self.env['product.template'].browse(int(
                self.env['ir.config_parameter'].sudo().get_param(
                    'producto_descuento_parameter')) or False).product_variant_id

            for line in this.invoice_line_ids:
                if line.product_id.id == producto_de_descuento.id:
                    this.monto_descuento = line.price_total
                    this.por_descuento = line.name


    def descuentoFactura(self):
        for this in self:
            if this.descuento != 0:
                linea_descuento = False
                producto_de_descuento = self.env['product.template'].browse(int(
                    self.env['ir.config_parameter'].sudo().get_param(
                        'producto_descuento_parameter')) or False).product_variant_id

                if not producto_de_descuento:
                    raise ValidationError('Debe asignar un producto como argumento de descuento')
                total = 0
                for line in this.invoice_line_ids:
                        if not line.product_id.id == producto_de_descuento.id:
                            total += line.price_unit * line.quantity
                        else:
                            linea_descuento = line

                descuento = total / 100 * this.descuento * -1

                if linea_descuento:
                    linea_descuento.update(
                        {'price_unit': descuento})
                else:
                    line_descuento = {
                        'name': producto_de_descuento.name,
                        'product_id': producto_de_descuento.id,
                        'account_id' : producto_de_descuento.property_account_income_id.id,
                        'quantity': 1,
                        'price_unit': descuento,
                        'invoice_id': this.id
                    }
                    this.env['account.invoice.line'].create(line_descuento)

    def _fechaLetras(self):
        for this in self:
            if this.date_invoice:
                this.fecha_letras = this.date_invoice.strftime("%d de %B de %Y")
            else:
                this.fecha_letras = this.date_invoice

    def cantImpresiones(self):
        for this in self:
            if this.state == 'draft' or this.state == 'cancel':
                return True
            if this.type == 'out_invoice' and this.state != 'draft':
                this.cantidadImpresiones = this.cantidadImpresiones +1
                if this.cantidadImpresiones>6:
                    return True
                else:
                    return False

    def resetearImpresiones(self):
        for this in self:
            this.cantidadImpresiones = 0

    def _comisionIVA(self):
        for this in self:
            if this.amount_total <= 750000:
                this.comisionIVA = 8250
            elif 750000 < this.amount_total <= 2000000:
                this.comisionIVA = 10000
            elif 2000000 < this.amount_total <= 8000000:
                this.comisionIVA = 16500
            elif 8000000 < this.amount_total <= 15000000:
                this.comisionIVA = 19250
            elif 15000000 < this.amount_total <= 30000000:
                this.comisionIVA = 22000
            elif 30000000 < this.amount_total <= 40000000:
                this.comisionIVA = 27500
            elif 40000000 < this.amount_total <= 50000000:
                this.comisionIVA = 33000
            elif 50000000 < this.amount_total <= 60000000:
                this.comisionIVA = 38500
            elif this.amount_total > 60000000:
                this.comisionIVA = 71500


    def format_linea(self, linea=False):
        limite = int(self.env['ir.config_parameter'].sudo().get_param('interfaces_facturas.limite_caracteres')) # 27
        if not linea:
            return False
        else:
            linea_limitada = []
            linea_actual = ''
            c = 0
            for i in linea:
                c += 1
                linea_actual += i
                if c == limite:
                    linea_limitada.append(linea_actual)
                    linea_actual = ''
                    c = 0
            if linea_actual:linea_limitada.append(linea_actual)
            return linea_limitada

    def get_lineas(self):
        for this in self:
            lineas_para_reporte = []
            for linea in this.invoice_line_ids:
                lineas_para_reporte += this.format_linea(linea.name)
            if this.comment:
                lineas_para_reporte += this.format_linea(this.comment)
            lineas = math.ceil(len(lineas_para_reporte))
            if this.comment:
                lineas+=1
            if lineas >= 20:
                this.limite_excedido = True
            else:
                this.limite_excedido = False
            return lineas

    @api.model
    def create(self, vals):
        r = super(accountInvoice, self).create(vals)
        if r.descuento > 0:
            producto_de_descuento = self.env['product.template'].browse(int(
                self.env['ir.config_parameter'].sudo().get_param(
                    'producto_descuento_parameter')) or False).product_variant_id

            if not producto_de_descuento:
                raise ValidationError('Debe asignar un producto como argumento de descuento')
            total = 0
            for line in r.invoice_line_ids:
                if not line.product_id.id == producto_de_descuento.id:
                    total += line.price_unit * line.quantity

            descuento = total / 100 * r.descuento * -1

            line_descuento = {
                    'name': producto_de_descuento.name,
                    'product_id': producto_de_descuento.id,
                    'account_id': producto_de_descuento.property_account_income_id.id,
                    'quantity': 1,
                    'price_unit': descuento,
                    'invoice_id': r.id
                }
            r.env['account.invoice.line'].create(line_descuento)
        return r

    @api.multi
    def write(self, values):
        for this in self:
            r = super(accountInvoice, self).write(values)
            this.descuentoFactura()
            return r

    def action_invoice_open(self):
        for this in self:
            this.descuentoFactura()
            if not this.partner_id.vat:
                if this.partner_id.parent_id:
                    if this.partner_id.parent_id.vat:
                        raise ValidationError(
                            'El cliente no tiene RUC. No puede validar la factura')
                raise ValidationError(
                    'El cliente no tiene RUC. No puede validar la factura')
            if this.journal_id.facturas_sueltas == False and this.origin == False:
                raise ValidationError('En este diario no puede crear una factura que no proviene de ningún expediente')
            else:
                this.cantidadImpresiones = 0
                return super(accountInvoice, self).action_invoice_open()

    def _barcode(self):
        for this in self:
            num_factura = this.fake_number
            num_factura_array=num_factura.split("-")
            for index,elemento in enumerate(num_factura_array):
                #print(index)
                if len(elemento) < 3:
                    num_factura_array[index] = '0' + elemento
            num_factura_string = ''.join(num_factura_array)
            ##########################################################
            monto_total = str(this.amount_total+this.comisionIVA)
            importe_total_string = monto_total.replace('.','')+"0"
            if len(importe_total_string) < 11:
                for digit in range(len(importe_total_string),11):
                    importe_total_string = '0' + importe_total_string
            ##########################################################
            comisionIVA = str(this.comisionIVA)
            comisionIVA = comisionIVA + '00'
            # print(comisionIVA)
            if len(comisionIVA) < 7:
                for digit in range(len(comisionIVA),7):
                    comisionIVA = '0' + comisionIVA
            ##########################################################
            fecha_deseada_string = ""
            if this.date_due:
                fecha_deseada_string = datetime.datetime.strftime(this.date_due, '%Y%m%d')
            ##########################################################

            barcode='01114'+num_factura_string+fecha_deseada_string+importe_total_string+comisionIVA
            suma = 0
            for digit in range(1,len(barcode)):
                if int(digit) % 2 == 0:
                     producto = int(barcode[digit])*1
                else:
                     producto = int(barcode[digit])*3
                suma = suma + producto
            resto = suma % 10

            digito_verificador = 10 - resto

            if digito_verificador == 10:
                digito_verificador = 0

            this.barcode = barcode + str(digito_verificador)
