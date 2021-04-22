from odoo import fields,api,models,exceptions

class AccountInvoice(models.Model):
    _inherit='account.invoice'


    def action_invoice_open(self):
        for i in self:
            if not self.env.user.has_group('permisos_facturacion.grupo_facturacion'):
                raise exceptions.ValidationError('No tiene permisos para validar facturas. Contacte con su administrador')
            return super(AccountInvoice,i).action_invoice_open()