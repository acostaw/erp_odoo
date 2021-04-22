from odoo import api, fields, models


class MultiProduct(models.TransientModel):
    _name = 'multi.product'

    product_ids = fields.Many2many('product.product', string="Productos")

    def add_product(self):
        for line in self.product_ids:
            self.env['sale.order.line'].create({
                'product_id': line.id,
                'order_id': self._context.get('active_id')
            })
        return
