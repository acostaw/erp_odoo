# -*- coding: utf-8 -*-

from odoo import fields, api, models, exceptions
from odoo.exceptions import ValidationError
from odoo.osv import expression

class MultaMetrologica(models.Model):
    _name = 'multa_metrologica_intn'

    name = fields.Char(string="Número de Resolucion", required=True)
    partner_id = fields.Many2one('res.partner', string='Cliente', readonly=True,
                                 states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, required=True)
    state = fields.Selection([
        ('draft', 'Pendiente'),
        ('done', 'Facturado'),
    ], string='Estado', readonly=True,default='draft')

    jornales = fields.Integer(string="Cantidad de Jornales")
    resolucion_pdf = fields.Binary(string="Resolución en PDF")
    pdf_name = fields.Char(string="Resolución en PDF")
    multa_origen = fields.Many2one('account.invoice', string='Factura Multa')

    invoice_count = fields.Integer(string='Invoice Count', compute='_get_invoiced', readonly=True)
    invoice_ids = fields.Many2many("account.invoice", string='Invoices', compute="_get_invoiced", readonly=True,
                                   copy=False)

    @api.model
    def calcular_datos(self, multa):
            return {
                'partner_id': multa.partner_id,
                'jornales': multa.jornales
            }

    def button_wizard_factura(self):
        view = self.env.ref('multa_metrologica_intn.wizard_factura_form')

        return{
            'name': 'Registrar factura de multa metrológica',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'multa_metrologica_intn.wizard_factura',
            'context': {'default_multa_origen': self.id},
            'view_id': view.id,
            'target': 'new'
        }

    @api.multi
    def unlink(self):
        for this in self:
            if this.multa_origen and (this.multa_origen.state != 'draft' and this.multa_origen.state != 'cancel'):
                raise exceptions.ValidationError(
                    'No puede eliminar una resolucion que tenga una factura asociada.')



    @api.depends('state')
    def _get_invoiced(self):
        for order in self:
            invoice_ids = self.env['account.invoice'].search(
            [('type', '=', 'out_invoice'), ('multa_origen', '=', order.id)])

            order.update({
                'invoice_count': len(set(invoice_ids.ids)),
                'invoice_ids': invoice_ids.ids
            })

    @api.multi
    def action_view_invoice(self):
        invoices = self.mapped('invoice_ids')
        action = self.env.ref('account.action_invoice_tree1').read()[0]
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            form_view = [(self.env.ref('account.invoice_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = invoices.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
