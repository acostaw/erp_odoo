from odoo import api, fields, models


class MultiProductInvoice(models.TransientModel):
    _name = 'multi.product.invoice'

    product_ids = fields.Many2many('product.product', string="Productos")

    def add_product(self):
        for line in self.product_ids:
            account = line.property_account_income_id or line.categ_id.property_account_income_categ_id
            self.env['account.invoice.line'].create({
                'product_id': line.id,
                'name' :line.name,
                'price_unit':line.lst_price,
                'account_id':account.id,
                'uom_id': line.uom_id.id,
                'invoice_id': self._context.get('active_id'),
                'invoice_line_tax_ids': [(6, 0, line.taxes_id.ids)],
                'select':True
            })
        return
