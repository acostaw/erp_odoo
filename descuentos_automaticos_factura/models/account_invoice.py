from odoo import api, fields, models, exceptions


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def create(self, vals):
        res = super(AccountInvoice, self).create(vals)
        promocion_activa = self.env['ir.config_parameter'].sudo(
        ).get_param('descuentos_automaticos')
        if promocion_activa in ['True', 'true', '1', 's', 'S']:
            res.compute_taxes()
        return res

    def write(self, vals):
        for invoice in self:
            res = super(AccountInvoice, invoice).write(vals)
            promocion_activa = self.env['ir.config_parameter'].sudo(
            ).get_param('descuentos_automaticos')
            if promocion_activa in ['True', 'true', '1', 's', 'S'] and not invoice._context.get('actualiza_taxes'):
                invoice.with_context(actualiza_taxes=True).compute_taxes()
            return res

    @api.depends('payment_term_id' 'invoice_line_ids', 'type', 'origin', 'journal_id')
    @api.onchange('payment_term_id', 'invoice_line_ids', 'type', 'origin', 'journal_id')
    def aplica_descuento(self):
        promocion_activa = self.env['ir.config_parameter'].sudo(
        ).get_param('descuentos_automaticos')
        if (
                self.payment_term_id.name == 'Contado' or not self.payment_term_id) and self.type == 'out_invoice' and not self.journal_id.diario_multa and promocion_activa in [
            'True', 'true', '1', 's', 'S'] and self.invoice_line_ids:
            product_id = None
            producto = self.env['ir.config_parameter'].sudo(
            ).get_param('producto_descuentos_automaticos')
            nombre_promocion = self.env['ir.config_parameter'].sudo(
            ).get_param('nombre_descuentos_automaticos')
            if producto:
                product_id = self.env['product.product'].browse(int(producto))
            else:
                raise exceptions.ValidationError(
                    'No se definió un producto para descuentos automáticos. Vaya a parametros del sistema')
            if product_id:
                porcentaje = self.env['ir.config_parameter'].sudo(
                ).get_param('porcentaje_descuentos_automaticos')
                if float(porcentaje):
                    porcentaje = float(porcentaje)
                    lineas_factura = self.invoice_line_ids.filtered(
                        lambda x: x.product_id.id != product_id.id and x.price_total > 0)
                    montos_impuestos = []
                    for tax in list(set(lineas_factura.mapped('invoice_line_tax_ids'))):
                        montos_impuestos.append({'tax': tax, 'total': sum(
                            lineas_factura.filtered(lambda z: tax.id in z.invoice_line_tax_ids.ids).mapped('price_total'))})
                    for mon in montos_impuestos:
                        tax_id = mon.get('tax')
                        tax = []
                        tax.append(tax_id.id)
                        price_unit = mon.get('total') * porcentaje / 100 * -1
                        existe_descuento = self.invoice_line_ids.filtered(
                            lambda x: x.product_id.id == product_id.id and tax_id in x.invoice_line_tax_ids)
                        if not existe_descuento:
                            self.update({'invoice_line_ids': [(0, 0, {
                                'product_id': product_id.id,
                                'uom_id': product_id.uom_id.id,
                                'name': nombre_promocion,
                                'quantity': 1,
                                'price_unit': price_unit,
                                'invoice_line_tax_ids': [(6, 0, tax)],
                                'account_id':  product_id.property_account_income_id.id or  self.journal_id.default_credit_account_id.id,
                                #'invoice_line_tax_ids': [(6, 0, product_id.taxes_id.ids)]
                            })]})
                        else:
                            self.update({'invoice_line_ids': [(1, existe_descuento.id, {
                                'product_id': product_id.id,
                                'name': nombre_promocion,
                                'uom_id': product_id.uom_id.id,
                                'quantity': 1,
                                'price_unit': price_unit,
                                'account_id': product_id.property_account_income_id.id or self.journal_id.default_credit_account_id.id,
                                'invoice_line_tax_ids': [(6, 0, tax)],
                                # 'invoice_line_tax_ids': [(6, 0, product_id.taxes_id.ids)]
                            })]})
                    # total_lineas_factura = sum(self.invoice_line_ids.filtered(
                    #     lambda x: x.product_id.id != product_id.id and x.price_total > 0).mapped(
                    #     lambda z: z.price_total))
                    # monto_descuento = 0
                    # if total_lineas_factura > 0:
                    #     monto_descuento = total_lineas_factura * porcentaje / 100 * -1
                    # existe_descuento = self.invoice_line_ids.filtered(
                    #     lambda x: x.product_id.id == product_id.id)
                    # if not existe_descuento:
                    #     self.update({'invoice_line_ids': [(0, 0, {
                    #         'product_id': product_id.id,
                    #         'uom_id': product_id.uom_id.id,
                    #         'name': nombre_promocion,
                    #         'quantity': 1,
                    #         'price_unit': monto_descuento,
                    #         'account_id': product_id.property_account_income_id.id or self.journal_id.default_credit_account_id.id,
                    #         'invoice_line_tax_ids': [(6, 0, product_id.taxes_id.ids)]
                    #     })]})
                    # else:
                    #     self.update({'invoice_line_ids': [(1, existe_descuento.id, {
                    #         'product_id': product_id.id,
                    #         'name': nombre_promocion,
                    #         'uom_id': product_id.uom_id.id,
                    #         'quantity': 1,
                    #         'price_unit': monto_descuento,
                    #         'account_id': product_id.property_account_income_id.id or self.journal_id.default_credit_account_id.id,
                    #         'invoice_line_tax_ids': [(6, 0, product_id.taxes_id.ids)]
                    #     })]})
                else:
                    raise exceptions.ValidationError(
                        'Porcentaje de descuentos automáticos incorrecto. Vaya a parametros del sistema')
            else:
                raise exceptions.ValidationError(
                    'No se encontró el producto de descuento automático. Vaya a parametros del sistema')
            return
        else:
            producto = self.env['ir.config_parameter'].sudo(
            ).get_param('producto_descuentos_automaticos')
            if producto:
                product_id = self.env['product.product'].browse(int(producto))
                existe_descuento = self.invoice_line_ids.filtered(
                    lambda x: x.product_id.id == product_id.id)
                if existe_descuento:
                    for ex in existe_descuento:
                        self.update(
                            {'invoice_line_ids': [(3, ex.id, 0)]})
                    return
                else:
                    return
