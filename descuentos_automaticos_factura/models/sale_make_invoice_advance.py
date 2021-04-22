from odoo import api, fields, models,exceptions


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    
    @api.multi
    def create_invoices(self):
        for i in self:
            res=super(SaleAdvancePaymentInv,i).create_invoices()
            sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
            if sale_orders:
                for order in sale_orders:
                    for invoice in order.invoice_ids:
                        invoice.aplica_descuento()
            return res