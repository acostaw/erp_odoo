from odoo import models, fields, api
from odoo.exceptions import ValidationError


class saleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    @api.multi
    def create_invoices(self):
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))

        for order in sale_orders:
            if order.pago_exonerado:
                raise ValidationError(
                    'No puede crear una factura para este expediente, el cobro total fue exonerado via resolucion.')
        super(saleAdvancePaymentInv, self).create_invoices()

    #@api.multi
    #def _create_invoice(self,order,so_line,amount):
    #    invoice=super(saleAdvancePaymentInv,self)._create_invoice(order,so_line,amount)
    #    recevaible=invoice.get('account_id')
    #    if not recevaible:
    #        invoice['account_id']=invoice.partner_id.property_account_receivable_id.id or invoice.partner_id.commercial_partner_id.property_account_receivable_id.id
    #    
    #    return invoice