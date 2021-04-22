from odoo import fields, api, models, exceptions
from datetime import date
import math

from . import amount_to_text_spanish
import locale


class PaymentGroup(models.Model):
    _name = 'grupo_account_payment.payment.group'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Grupo de pago'
    _order = 'name desc'

    name = fields.Char('Número', default="Borrador",
                       track_visibility='onchange', copy=False)
    partner_id = fields.Many2one(
        'res.partner', string='Empresa', required=True, track_visibility='onchange')
    payment_ids = fields.One2many(
        'account.payment', 'payment_group_id', string='Lineas de pago', copy="False", track_visibility='onchange')
    fecha = fields.Date(
        string='Fecha', default=lambda self:fields.Date.today(), required=True, track_visibility='onchange')
    user_id = fields.Many2one(
        'res.users', string="Usuario", default=lambda self: self.env.user)
    currency_id = fields.Many2one('res.currency', string='Moneda',
                                  default=lambda self: self.env.user.company_id.currency_id, groups='base.group_multi_currency', track_visibility='onchange')
    company_id = fields.Many2one(
        'res.company', string='Compañia', default=lambda self: self.env.user.company_id, track_visibility='onchange')
    amount_total = fields.Monetary(
        string='Total de pagos', compute='compute_total', default=0, store=True, track_visibility='onchange')
    amount_total_company_signed = fields.Monetary(
        string='Total en moneda de la compañia', default=0, compute='compute_total', store=True)
    payment_type = fields.Selection(string="Tipo de pago", selection=[(
        'inbound', 'Inbound'), ('outbound', 'Outbound')], required=True)
    memo = fields.Char(string="Memo", track_visibility='onchange')
    state = fields.Selection(string='Estado', selection=[(
        'draft', 'Borrador'), ('done', 'Confirmado'), ('cancel', 'Cancelado')], default='draft', track_visibility='onchange')
    invoice_ids = fields.Many2many(
        'account.invoice', 'invoice_invoice_ids', string="Facturas", copy="False", track_visibility='onchange')
    amount_total_selected = fields.Monetary(
        string='Total deudas seleccionadas', compute='compute_total', default=0, store=True, track_visibility='onchange')
    cantRecibos = fields.Integer(compute="_cantRecibos")

    fecha_letras = fields.Char(compute='_fechaLetras')
    diferencia_menor = fields.Boolean(default=False,store=False)

    paid_invoice_ids = fields.Many2many(
        'account.invoice', compute="compute_paid_invoices",store=False)


    refund_ids = fields.Many2many(
        'account.invoice', 'invoice_refunds_ids', string="Notas de Crédito", copy="False")

    tipo_recibo = fields.Char('Tipo de Recibo', copy=False, compute="compute_tipo_factura")

    #locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8')


    def compute_tipo_factura(self):
        for this in self:
            for index,fac in enumerate(this.paid_invoice_ids):
                if fac.tipo_factura == 'contado':
                    this.tipo_recibo = 'contado'
                else:
                    this.tipo_recibo = 'credito'
                if index == 0:
                    break


    def compute_paid_invoices(self):
        for recibo in self:
            invoices = []
            invs = []
            for i in recibo.payment_ids:
                for j in i.reconciled_invoice_ids:
                    invoices.append((4, j.id, 0))
            for factura in recibo.invoice_ids:
                for payment in factura.payment_move_line_ids:
                    if factura.type in ('out_invoice', 'in_refund'):
                        amount = sum(
                            [p.amount for p in payment.matched_debit_ids if p.debit_move_id in factura.move_id.line_ids])
                        amount_currency = sum([p.amount_currency for p in payment.matched_debit_ids if
                                               p.debit_move_id in factura.move_id.line_ids])
                        if payment.matched_debit_ids:
                            payment_currency_id = all([p.currency_id == payment.matched_debit_ids[0].currency_id for p in
                                                       payment.matched_debit_ids]) and payment.matched_debit_ids[
                                                      0].currency_id or False
                            if payment_currency_id and payment_currency_id == factura.currency_id:
                                amount_to_show = amount_currency
                            else:
                                amount_to_show = payment.company_id.currency_id.with_context(date=payment.date).compute(
                                    amount, factura.currency_id)
                            for nc in recibo.refund_ids:
                                if payment.move_id.name == nc.number:
                                    invs.append(factura)
                                    invoices.append((4, factura.id, 0))
            recibo.paid_invoice_ids = invoices

    def _fechaLetras(self):
        for this in self:
            this.fecha_letras = this.fecha.strftime("%d de %B de %Y")

    @api.one
    def _cantRecibos(self):
        for this in self:
            #print (this.invoice_ids[0])
            if len(this.paid_invoice_ids) > 8:
                this.cantRecibos = math.ceil(len(this.paid_invoice_ids)/8)
            else:
                this.cantRecibos = 1

    @api.onchange('partner_id')
    @api.depends('payment_ids')
    def onchange_partner(self):
        for i in self:
            if i.payment_ids:
                for j in i.payment_ids:
                    j.update({'partner_id': i.partner_id.id})
            if i.invoice_ids and not i.invoice_ids.filtered(lambda x: x.partner_id == i.partner_id):
                i.update({'invoice_ids': [(5, 0, 0)]})
            if i.refund_ids and not i.refund_ids.filtered(lambda x: x.partner_id == i.partner_id):
                i.update({'invoice_ids': [(5, 0, 0)]})

    @api.onchange('fecha')
    @api.depends('payment_ids')
    def onchange_fecha(self):
        for i in self:
            if i.payment_ids:
                for j in i.payment_ids:
                    j.update({'payment_date': i.fecha})

    @api.depends('payment_ids', 'refund_ids','invoice_ids')
    @api.onchange('payment_ids', 'refund_ids','invoice_ids')
    def compute_total(self):
        for i in self:
            res = {}
            refund_residual =  0
            i.amount_total = 0
            i.amount_total_selected = 0
            for payment in i.payment_ids:
                i.amount_total += payment.amount
            for refund in i.refund_ids:
                refund_residual = refund_residual + refund.residual
                i.amount_total += refund.residual
            for invoice in i.invoice_ids:
                i.amount_total_selected += invoice.residual
            if i.amount_total and i.amount_total_selected > i.amount_total:
                i.diferencia_menor = True
            elif i.amount_total > i.amount_total_selected:
                i.diferencia_menor = False
            else:
                i.diferencia_menor = False

            if i.amount_total > i.amount_total_selected and refund_residual < i.amount_total_selected:
                # raise exceptions.ValidationError(
                #     ('El monto pagado no puede ser mayor al monto total de las facturas seleccionadas'))
                res = {'warning': {
                    'title': ('Advertencia!'),
                    'message': ('El monto pagado no puede ser mayor al monto total de las facturas seleccionadas')
                }
                }
            if res:
                return res

    @api.depends('payment_type')
    def genera_secuencia(self):
        if self.payment_type == 'inbound':
            aquiPago = False
            for payment in self.payment_ids:
                if payment.tipo_pago == 'aquiPago':
                    aquiPago = True
            if self.tipo_recibo == 'contado' or aquiPago == True:
                seq = self.sudo().env['ir.sequence'].next_by_code('seq_recibo_contado')
            elif self.tipo_recibo == 'credito' and aquiPago == False:
                seq = self.sudo().env['ir.sequence'].next_by_code('seq_recibo_credito')
            # seq = self.sudo().env['ir.sequence'].next_by_code('seq_recibo')
        elif self.payment_type == 'outbound':
            seq = self.sudo().env['ir.sequence'].next_by_code('seq_orden_pago')
        return seq

    def button_confirmar(self):
        for i in self:
            facturas_contado = False
            facturas_credito = False
            for fac in i.invoice_ids:
                if fac.tipo_factura == 'contado':
                    facturas_contado = True
                else:
                    facturas_credito = True
            if facturas_contado and facturas_credito:
                raise exceptions.ValidationError(
                    'No puede pagar en un mismo recibo facturas al Contado y facturas a Crédito.')
            if not i.partner_id.property_account_receivable_id:
                i.partner_id.property_account_receivable_id = i.partner_id.parent_id.property_account_receivable_id
            if not i.partner_id.property_account_payable_id:
                i.partner_id.property_account_payable_id = i.partner_id.parent_id.property_account_payable_id
            for j in i.payment_ids:
                j.post()
                if j.payment_type == 'inbound':
                    movimiento = j.move_line_ids.filtered(
                        lambda z: z.debit > 0)
                elif j.payment_type == 'outbound':
                    movimiento = j.move_line_ids.filtered(
                        lambda z: z.credit > 0)
                else:
                    movimiento = j.move_line_ids
                for x in movimiento:
                    referencia = j.tipo_pago.capitalize()+" "
                    if j.bank_id:
                        referencia += j.bank_id.name+" "
                    if j.nro_cheque:
                        referencia += j.nro_cheque+" "
                    if j.nro_documento:
                        referencia += j.nro_documento+" "
                    x.write({'ref': referencia})
            for inv in i.invoice_ids.sorted(key=lambda x: x.date_due):
                for nc in i.refund_ids:
                    for inv in i.invoice_ids:
                        for aml in nc.move_id.line_ids.filtered(lambda x :x.account_id.user_type_id.type in ['payable','receivable'] and not x.reconciled):
                            inv.register_payment(aml)
                for payment in i.payment_ids:
                    for ml in payment.move_line_ids.filtered(lambda x: x.account_id.user_type_id.type in ['payable', 'receivable'] and not x.reconciled):
                        inv.register_payment(ml)
            i.write({'state': 'done'})

    def button_cancelar(self):
        if not self.env.user.has_group('grupo_account_payment.group_cancelar_recibos'):
            raise exceptions.ValidationError('No tiene permisos para cancelar recibos. Contacte con su administrador')
        for i in self.payment_ids:
            i.cancel()
        self.write({'state': 'cancel'})

    def button_draft(self):
        for i in self.payment_ids:
            i.action_draft()
        self.write({'state': 'draft'})

    def asigna_nombre(self):
        for i in self:
            if self.name and self.name == 'Borrador':
                new_name = i.genera_secuencia()
                for j in i.payment_ids:
                    j.write({'name': new_name})
                    for x in j.move_line_ids:
                        x.write({'name': new_name})
                i.write({'name': new_name})
            else:
                return

    def write(self, vals):
        for i in self:
            r = super(PaymentGroup, i).write(vals)
            if vals.get('state') and vals.get('state') == 'done':
                i.asigna_nombre()
            return super(PaymentGroup, i).write(vals)

    @api.model
    def create(self, vals):
        if vals.get('payment_type') == 'inbound':
            flag = self.env.user.has_group(
                'grupo_account_payment.grupo_cobrador')
            if not flag:
                raise exceptions.ValidationError(
                    ('No tiene permisos para registrar recibos'))
        if vals.get('payment_type') == 'outbound':
            flag = self.env.user.has_group(
                'grupo_account_payment.grupo_orden_pago')
            if not flag:
                raise exceptions.ValidationError(
                    ('No tiene permisos para registrar ordenes de pago'))
        if not vals.get('payment_type'):
            raise exceptions.ValidationError(
                ('Tipo de pago no definido. Contacte con su administrador'))
        return super(PaymentGroup, self).create(vals)

    @api.multi
    def amount_to_text_esp(self, amount):
        MONEDA_SINGULAR = 'bolivar'
        MONEDA_PLURAL = 'bolivares'

        CENTIMOS_SINGULAR = 'centimo'
        CENTIMOS_PLURAL = 'centimos'

        MAX_NUMERO = 999999999999

        UNIDADES = (
            'cero',
            'uno',
            'dos',
            'tres',
            'cuatro',
            'cinco',
            'seis',
            'siete',
            'ocho',
            'nueve'
        )

        DECENAS = (
            'diez',
            'once',
            'doce',
            'trece',
            'catorce',
            'quince',
            'dieciseis',
            'diecisiete',
            'dieciocho',
            'diecinueve'
        )

        DIEZ_DIEZ = (
            'cero',
            'diez',
            'veinte',
            'treinta',
            'cuarenta',
            'cincuenta',
            'sesenta',
            'setenta',
            'ochenta',
            'noventa'
        )

        CIENTOS = (
            '_',
            'ciento',
            'doscientos',
            'trescientos',
            'cuatroscientos',
            'quinientos',
            'seiscientos',
            'setecientos',
            'ochocientos',
            'novecientos'
        )

        def numero_a_letras(numero):
            numero_entero = int(numero)
            if numero_entero > MAX_NUMERO:
                raise OverflowError('Número demasiado alto')
            if numero_entero < 0:
                return 'menos %s' % numero_a_letras(abs(numero))
            letras_decimal = ''
            parte_decimal = int(
                round((abs(numero) - abs(numero_entero)) * 100))
            if parte_decimal > 9:
                letras_decimal = 'punto %s' % numero_a_letras(parte_decimal)
            elif parte_decimal > 0:
                letras_decimal = 'punto cero %s' % numero_a_letras(
                    parte_decimal)
            if (numero_entero <= 99):
                resultado = leer_decenas(numero_entero)
            elif (numero_entero <= 999):
                resultado = leer_centenas(numero_entero)
            elif (numero_entero <= 999999):
                resultado = leer_miles(numero_entero)
            elif (numero_entero <= 999999999):
                resultado = leer_millones(numero_entero)
            else:
                resultado = leer_millardos(numero_entero)
            resultado = resultado.replace('uno mil', 'un mil')
            resultado = resultado.strip()
            resultado = resultado.replace(' _ ', ' ')
            resultado = resultado.replace('  ', ' ')
            if parte_decimal > 0:
                resultado = '%s %s' % (resultado, letras_decimal)
            return resultado.upper()

        def numero_a_moneda(numero):
            numero_entero = int(numero)
            parte_decimal = int(
                round((abs(numero) - abs(numero_entero)) * 100))
            centimos = ''
            if parte_decimal == 1:
                centimos = CENTIMOS_SINGULAR
            else:
                centimos = CENTIMOS_PLURAL
            moneda = ''
            if numero_entero == 1:
                moneda = MONEDA_SINGULAR
            else:
                moneda = MONEDA_PLURAL
            letras = numero_a_letras(numero_entero)
            letras = letras.replace('uno', 'un')
            letras_decimal = 'con %s %s' % (numero_a_letras(
                parte_decimal).replace('uno', 'un'), centimos)
            letras = '%s %s %s' % (letras, moneda, letras_decimal)
            return letras

        def leer_decenas(numero):
            if numero < 10:
                return UNIDADES[numero]
            decena, unidad = divmod(numero, 10)
            if numero <= 19:
                resultado = DECENAS[unidad]
            elif numero <= 29:
                resultado = 'veinti%s' % UNIDADES[unidad]
            else:
                resultado = DIEZ_DIEZ[decena]
                if unidad > 0:
                    resultado = '%s y %s' % (resultado, UNIDADES[unidad])
            return resultado

        def leer_centenas(numero):
            centena, decena = divmod(numero, 100)
            if numero == 0:
                resultado = 'cien'
            else:
                resultado = CIENTOS[centena]
                if decena > 0:
                    resultado = '%s %s' % (resultado, leer_decenas(decena))
            return resultado

        def leer_miles(numero):
            millar, centena = divmod(numero, 1000)
            resultado = ''
            if (millar == 1):
                resultado = ''
            if (millar >= 2) and (millar <= 9):
                resultado = UNIDADES[millar]
            elif (millar >= 10) and (millar <= 99):
                resultado = leer_decenas(millar)
            elif (millar >= 100) and (millar <= 999):
                resultado = leer_centenas(millar)
            resultado = '%s mil' % resultado
            if centena > 0:
                resultado = '%s %s' % (resultado, leer_centenas(centena))
            return resultado

        def leer_millones(numero):
            millon, millar = divmod(numero, 1000000)
            resultado = ''
            if (millon == 1):
                resultado = ' un millon '
            if (millon >= 2) and (millon <= 9):
                resultado = UNIDADES[millon]
            elif (millon >= 10) and (millon <= 99):
                resultado = leer_decenas(millon)
            elif (millon >= 100) and (millon <= 999):
                resultado = leer_centenas(millon)
            if millon > 1:
                resultado = '%s millones' % resultado
            if (millar > 0) and (millar <= 999):
                resultado = '%s %s' % (resultado, leer_centenas(millar))
            elif (millar >= 1000) and (millar <= 999999):
                resultado = '%s %s' % (resultado, leer_miles(millar))
            return resultado

        def leer_millardos(numero):
            millardo, millon = divmod(numero, 1000000)
            return '%s millones %s' % (leer_miles(millardo), leer_millones(millon))

        convert_amount_in_words = numero_a_letras(amount)
        return convert_amount_in_words

    @api.multi
    def amount_to_text(self, amount, currency):
        convert_amount_in_words = amount_to_text_spanish.to_word(amount)
        return convert_amount_in_words

    def _notasdeCredito(self):
        for recibo in self:
            notasdeCredito = []
            for factura in recibo.paid_invoice_ids:
                for payment in factura.payment_move_line_ids:
                    if factura.type in ('out_invoice', 'in_refund'):
                        amount = sum(
                            [p.amount for p in payment.matched_debit_ids if p.debit_move_id in factura.move_id.line_ids])
                        amount_currency = sum([p.amount_currency for p in payment.matched_debit_ids if
                                               p.debit_move_id in factura.move_id.line_ids])
                        if payment.matched_debit_ids:
                            payment_currency_id = all([p.currency_id == payment.matched_debit_ids[0].currency_id for p in
                                                       payment.matched_debit_ids]) and payment.matched_debit_ids[
                                                      0].currency_id or False
                            if payment_currency_id and payment_currency_id == factura.currency_id:
                                amount_to_show = amount_currency
                            else:
                                amount_to_show = payment.company_id.currency_id.with_context(date=payment.date).compute(
                                    amount, factura.currency_id)
                            if payment.invoice_id in recibo.refund_ids:
                                notasdeCredito.append(
                                    {'tipo': 'Nota de Crédito', 'nro_documento': payment.move_id.name,
                                     'amount': amount_to_show})
        return notasdeCredito


class ReporteAbstract(models.AbstractModel):
    _name = 'report.grupo_account_payment.template_pagos'

    @api.model
    def _get_report_values(self, docids, data=None):
        report_name = 'grupo_account_payment.template_pagos'
        report = self.env['ir.actions.report']._get_report_from_name(report_name)
        return {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': self.env[report.model].browse(docids),
            'notasdeCredito': self.env['grupo_account_payment.payment.group'].browse(docids)._notasdeCredito()
        }
