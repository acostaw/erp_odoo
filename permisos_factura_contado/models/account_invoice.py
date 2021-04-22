from odoo import fields,api,models,exceptions

class AccountInvoice(models.Model):
    _inherit='account.invoice'


    def action_invoice_open(self):
        for i in self:
            if not i.date_due:
                i.write({'date_due':fields.Date.today()})
            if not i.date_invoice:
                i.write({'date_invoice':fields.Date.today()})
            if i.date_due <= i.date_invoice and not self.env.user.has_group('permisos_factura_contado.emite_facturas_contado'):
                raise exceptions.ValidationError('No tiene permisos para emitir facturas contado. Cambie el plazo de pago o la fecha de vencimiento de la factura')
            return super(AccountInvoice,i).action_invoice_open()