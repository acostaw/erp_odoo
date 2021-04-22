from odoo import fields, api, models, exceptions


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def action_invoice_open(self):
        for i in self:
            if i.type == 'out_invoice':
                if i.origin:
                    order = self.env['sale.order'].search(
                        [('name', '=', i.origin)])
                    facturas = order.invoice_ids.filtered(
                        lambda x: x.id != i.id and x.state in ['open', 'paid'])
                    if order and len(order) == 1 and not order.pago_exonerado and not facturas:
                        mrps = self.env['mrp.production'].search(
                            [('state', '=', 'confirmed'), ('origin', '=', order.name)])
                        for m in mrps:
                            m.write({'name': order.name+'/'+m.name})
                            m.button_plan()
            return super(AccountInvoice, self).action_invoice_open()

    def action_invoice_cancel(self):
        for i in self:
            if i.type == 'out_invoice':
                if i.origin:
                    order = self.env['sale.order'].search(
                        [('name', '=', i.origin)])
                    if order:
                        workorders = self._cr.execute("UPDATE mrp_workorder SET state='pending' WHERE sale_order_id = '" + order.name + "'")
                        mrps = self.env['mrp.production'].search(
                            [('origin', '=', order.name)])
                        if mrps:
                            for prod in mrps:
                                if prod.finished_move_line_ids:
                                    for prod_finalizado in prod.finished_move_line_ids:
                                        prod_finalizado.write({'qty_done':0})
                                prod.action_cancel()
            return super(AccountInvoice, self).action_invoice_cancel()



