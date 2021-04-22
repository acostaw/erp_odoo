from odoo import api,fields,models
from . import amount_to_text_spanish

class AccountInvoice(models.Model):
    _inherit='account.invoice'


    @api.multi
    def amount_to_text(self, amount, currency):
        convert_amount_in_words = amount_to_text_spanish.to_word(amount)
        return convert_amount_in_words


    @api.multi
    def invoice_print(self):
        """ Print the invoice and mark it as sent, so that we can see more
            easily the next step of the workflow
        """
        if self.type=='out_invoice':
            self.ensure_one()
            self.sent = True
            return self.env.ref('interfaces_facturas.facturas_interfaces').report_action(self)

