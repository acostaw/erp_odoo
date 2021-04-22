# from odoo import fields, api, models, exceptions
from odoo import api, fields, models, exceptions, _


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    payment_group_id = fields.Many2one(
        'grupo_account_payment.payment.group', string="Grupo de pago")
    tipo_pago = fields.Selection(string="Tipo de pago", selection=[('efectivo', 'Efectivo'), ('cheque', 'Cheque'),
                                                                   ('retencion', 'Retención'), (
                                                                       'transferencia', 'Transferencia'),
                                                                   ('descuentos', 'Descuentos'), ('deposito', 'Depósito bancario'), ('aquiPago', 'Aquí Pago'), ('otro', 'Otro')], required=False)
    bank_id = fields.Many2one('res.bank', string="Banco")
    nro_cheque = fields.Char(string='Nro. cheque')
    fecha_cheque = fields.Date(string='Fecha del cheque')
    fecha_venc_cheque = fields.Date(string='Fecha de vencimiento del cheque')
    nro_documento = fields.Char(string="Nro. de documento")
    nro_documento_cliente = fields.Char(string="Nro. de documento del Cliente")

    paid_invoice_ids = fields.Many2many(
        'account.invoice', compute="compute_paid_invoices", store=False)

    tipo_recibo = fields.Char(
        'Tipo de Recibo', copy=False, related="payment_group_id.tipo_recibo")

    def compute_tipo_factura(self):
        for this in self:
            this.tipo_recibo = this.payment_group_id.tipo_recibo

    def compute_paid_invoices(self):
        for this in self:
            recibo = self.env['grupo_account_payment.payment.group'].search(
                [('id', '=', this.payment_group_id.id)])
            invoices = []
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
                                    invoices.append((4, factura.id, 0))
            this.paid_invoice_ids = invoices

    @api.depends('nro_documento', 'tipo_pago')
    @api.onchange('nro_documento')
    def busca_transferencia_duplicada(self):
        duplicados=[]
        if self.tipo_pago == 'transferencia':
            duplicados = self.env['account.payment'].search([('tipo_pago', '=', 'transferencia'), ('state', 'not in', [
                                                            'draft', 'cancel']), ('nro_documento', '=', self.nro_documento.strip())])

        if duplicados:
            duplicados_str = ""
            for i in duplicados:
                duplicados_str = duplicados_str+"%s | Cliente %s | Transferencia %s | Banco %s | Monto %s\n" % (
                    i.name, i.partner_id.name, i.nro_documento, i.bank_id.name, str(i.amount))
            raise exceptions.UserError("Transferencias ya existentes en:\n %s"%duplicados_str)

    @api.depends('nro_cheque')
    def valida_cheque_duplicado(self):
        if self.nro_cheque:
            duplicado = self.env['account.payment'].search([('company_id', '=', self.company_id.id), (
                'bank_id', '=', self.bank_id.id), ('nro_cheque', '=', self.nro_cheque), ('id', '!=', self.id)])
            if duplicado:
                raise exceptions.ValidationError(
                    'Cheque ya existente: '+self.bank_id.name+" "+self.nro_cheque)
        else:
            return

    # @api.constrains('nro_documento')
    # def valida_transferencia_duplicado(self):
    #     if self.nro_documento and self.tipo_pago =='transferencia':
    #         duplicado = self.env['account.payment'].search([('company_id', '=', self.company_id.id), (
    #             'bank_id', '=', self.bank_id.id), ('nro_documento', '=', self.nro_documento), ('id', '!=', self.id)])
    #         if duplicado:
    #             print(duplicado)
    #             # raise exceptions.ValidationError('Tranferencia ya existente: ' + self.bank_id.name + " " + self.nro_documento)
    
    @api.depends('nro_documento', 'tipo_pago')
    @api.onchange('nro_documento')
    def valida_transferencia_duplicado(self):
        res = {}
        if self.nro_documento and self.tipo_pago=='transferencia':
            duplicado = self.env['account.payment'].search([('company_id', '=', self.company_id.id), (
                'bank_id', '=', self.bank_id.id),('tipo_pago','=','transferencia'), ('nro_documento', '=', self.nro_documento.strip())])
            if duplicado:
                res = {'warning': {
                    'title': ('Tranferencia ya existente!'),
                    'message': ('Tranferencia ya existente: ' + self.bank_id.name + " " + self.nro_documento)
                }
                }
        if res:
            return res
