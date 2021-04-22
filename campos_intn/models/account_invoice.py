# -*- coding: utf-8 -*-

from odoo import models, fields, api,exceptions,_
import datetime


class ComentarioFactura(models.Model):
    _inherit = "account.invoice"
    comment = fields.Char(string='Observaciones', required=False, readonly=False)
    nro_contrato = fields.Char(string='Observaciones', compute='_nro_contrato')
    nro_resolucion = fields.Char(string='Observaciones', compute='_nro_resolucion')


    def _nro_contrato(self):
        for this in self:
            recs = self.browse()
            recs = self.env['sale.order'].search([['name', '=', this.origin]])
            this.nro_contrato = recs.contrato_id.name

    def _nro_resolucion(self):
        for this in self:
            recs = self.browse()
            recs = self.env['sale.order'].search([['name', '=', this.origin]])
            this.nro_resolucion = recs.resolucion_id.name



    @api.onchange('partner_id', 'company_id')
    def _onchange_partner_id(self):
        account_id = False
        payment_term_id = False
        fiscal_position = False
        bank_id = False
        warning = {}
        domain = {}
        company_id = self.company_id.id
        p = self.partner_id if not company_id else self.partner_id.with_context(force_company=company_id)
        type = self.type or self.env.context.get('type', 'out_invoice')
        if p:
            rec_account = p.property_account_receivable_id or p.commercial_partner_id.property_account_receivable_id
            pay_account = p.property_account_payable_id  or p.commercial_partner_id.property_account_payable_id
            if not rec_account and not pay_account:
                action = self.env.ref('account.action_account_config')
                msg = _('Cannot find a chart of accounts for this company, You should configure it. \nPlease go to Account Configuration.')
                raise exceptions.RedirectWarning(msg, action.id, _('Go to the configuration panel'))

            if type in ('in_invoice', 'in_refund'):
                account_id = pay_account.id
                payment_term_id = p.property_supplier_payment_term_id.id
            else:
                account_id = rec_account.id
                payment_term_id = p.property_payment_term_id.id

            delivery_partner_id = self.get_delivery_partner_id()
            fiscal_position = self.env['account.fiscal.position'].get_fiscal_position(self.partner_id.id, delivery_id=delivery_partner_id)

            # If partner has no warning, check its company
            if p.invoice_warn == 'no-message' and p.parent_id:
                p = p.parent_id
            if p.invoice_warn and p.invoice_warn != 'no-message':
                # Block if partner only has warning but parent company is blocked
                if p.invoice_warn != 'block' and p.parent_id and p.parent_id.invoice_warn == 'block':
                    p = p.parent_id
                warning = {
                    'title': _("Warning for %s") % p.name,
                    'message': p.invoice_warn_msg
                    }
                if p.invoice_warn == 'block':
                    self.partner_id = False

        self.account_id = account_id
        self.payment_term_id = payment_term_id
        self.date_due = False
        self.fiscal_position_id = fiscal_position

        if type in ('in_invoice', 'out_refund'):
            bank_ids = p.commercial_partner_id.bank_ids
            bank_id = bank_ids[0].id if bank_ids else False
            self.partner_bank_id = bank_id
            domain = {'partner_bank_id': [('id', 'in', bank_ids.ids)]}
        elif type == 'out_invoice':
            domain = {'partner_bank_id': [('partner_id.ref_company_ids', 'in', [self.company_id.id])]}

        res = {}
        if warning:
            res['warning'] = warning
        if domain:
            res['domain'] = domain
        return res
