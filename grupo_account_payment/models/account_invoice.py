from odoo import fields, api, models, exceptions
from odoo.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    tipo_factura = fields.Char(string='Tipo de Factura', compute='tipoFactura')

    def tipoFactura(self):
        for this in self:
            if this.date_due:
                if this.date_invoice==this.date_due:
                    this.tipo_factura = 'contado'
                else:
                    this.tipo_factura = 'credito'


    def button_pago(self):
        if self.type == 'out_invoice':
            flag = self.env.user.has_group(
                'grupo_account_payment.grupo_cobrador')
            if flag:
                view = self.env.ref(
                    'grupo_account_payment.grupo_account_payment_form_view')
                return {
                    'name': 'Registrar pago',
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'grupo_account_payment.payment.group',
                    'views': [(view.id, 'form')],
                    'view_id': view.id,
                    # 'target': 'new',
                    'context': {'default_payment_type': 'inbound', 'default_partner_id': self.partner_id.id,
                                'default_invoice_ids': self.ids},
                }
            else:
                raise UserError(
                    'Su usuario no cuenta con permisos para registrar pagos')
        elif self.type == 'in_invoice':
            flag = self.env['res.users'].has_group(
                'grupo_account_payment.grupo_orden_pago')
            if flag:
                view = self.env.ref(
                    'grupo_account_payment.grupo_account_payment_orden_form_view')
                return {
                    'name': 'Registrar pago',
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'grupo_account_payment.payment.group',
                    'views': [(view.id, 'form')],
                    'view_id': view.id,
                    # 'target': 'new',
                    'context': {'default_payment_type': 'outbound', 'default_partner_id': self.partner_id.id,
                                'default_invoice_ids': [(4, self.id, 0)]},
                }
            else:
                raise UserError(
                    'Su usuario no cuenta con permisos para registrar órdenes de pago')

    @api.model
    def button_pago_multi(self, facturas):
        if facturas[0].type == 'out_invoice':
            flag = self.env.user.has_group(
                'grupo_account_payment.grupo_cobrador')
            if flag:
                view = self.env.ref(
                    'grupo_account_payment.grupo_account_payment_form_view')
                return {
                    'name': 'Registrar pago',
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'grupo_account_payment.payment.group',
                    'views': [(view.id, 'form')],
                    'view_id': view.id,
                    # 'target': 'new',
                    'context': {'default_payment_type': 'inbound', 'default_partner_id': facturas[0].partner_id.id,
                                'default_invoice_ids': [(6, 0, facturas.ids)]},
                }
            else:
                raise UserError(
                    'Su usuario no cuenta con permisos para registrar pagos')

        elif facturas[0].type == 'in_invoice':
            flag = self.env.user.has_group(
                'grupo_account_payment.grupo_orden_pago')
            if flag:
                view = self.env.ref(
                    'grupo_account_payment.grupo_account_payment_orden_form_view')
                return {
                    'name': 'Registrar pago',
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'grupo_account_payment.payment.group',
                    'views': [(view.id, 'form')],
                    'view_id': view.id,
                    # 'target': 'new',
                    'context': {'default_payment_type': 'outbound', 'default_partner_id': self.partner_id.id,
                                'default_invoice_ids': [(6, 0, facturas.ids)]},
                }
            else:
                raise UserError(
                    'Su usuario no cuenta con permisos para registrar ordenes de pago')
