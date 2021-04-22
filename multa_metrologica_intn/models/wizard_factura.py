from odoo import fields, api, models, exceptions


class WizardFactura(models.TransientModel):
    _name = 'multa_metrologica_intn.wizard_factura'

    multa_origen = fields.Many2one(
        'multa_metrologica_intn', string="Resolucion Multa Metrologica")

    partner_id = fields.Many2one('res.partner', string='Cliente', readonly=True,
                                 states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})

    jornales = fields.Integer(string="Cantidad de Jornales", compute="datos")

    @api.depends('multa_origen')
    def datos(self):
        multa = self.multa_origen
        self.partner_id = multa.partner_id
        self.jornales = multa.jornales


    def button_confirmar(self):
            producto_multa_metrologica = self.env['product.template'].search(
                [('id', '=', 1)])
            if not producto_multa_metrologica:
                raise exceptions.ValidationError(
                    'Se debe establecer un producto para las multas metrologicas. Favor contacte con su administrador.')
            journal = self.env['account.journal'].search([('diario_multa', '!=', False)],limit=1)
            if not journal:
                raise exceptions.ValidationError(
                    'Se debe establecer un diario para las multas metrologicas. Favor contacte con su administrador.')
            for this in self:
                lines = [(0, 0, {
                    'product_id': producto_multa_metrologica.product_variant_id.id,
                    'name': producto_multa_metrologica.name,
                    'quantity': this.jornales,
                    'price_unit': producto_multa_metrologica.lst_price,
                    'account_id': producto_multa_metrologica.property_account_income_id.id,
                    'invoice_line_tax_ids': [[6, 0, producto_multa_metrologica.taxes_id.ids]]
                })]

                data = {
                    'partner_id': this.partner_id.id,
                    'date_invoice': fields.Date.today(),
                    'multa_origen': this.multa_origen.id,
                    'invoice_line_ids': lines,
                    'origin': this.multa_origen.name,
                    'state': 'draft',
                    'journal_id' : journal.id
                }
                multa_origen = self.env['account.invoice'].create(data)
                this.multa_origen.write({'multa_origen': multa_origen.id})
                view = self.env.ref('account.invoice_form')
                return {
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'account.invoice',
                    'res_id': multa_origen.id,
                    'view_id': view.id,
                }
