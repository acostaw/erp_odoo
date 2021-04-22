from odoo import fields, api, models, exceptions


class AccountCajaSession(models.Model):
    _name = 'account.caja.session'
    _order = 'id desc'

    name = fields.Char(string="Número", required=True,
                       default='Nuevo', readonly=True)
    statement_ids = fields.Many2many(
        'account.bank.statement', string="Extractos")
    fecha_hora_inicio = fields.Datetime(
        'Fecha/hora inicio', default=lambda self: fields.Datetime.now())
    fecha_hora_fin = fields.Datetime('Fecha/hora fin')
    user_id = fields.Many2one(
        'res.users', string="Cajero", required=True, default=lambda self: self.env.user)
    state = fields.Selection(string="Estado", selection=[('apertura', 'Apertura'), (
        'proceso', 'En proceso'), ('cierre', 'Cierre'), ('done', 'Cerrada y contabilizada')], default='apertura')
    caja_id = fields.Many2one('account.caja', string="Caja", required=True)
    company_id = fields.Many2one(
        'res.company', string="Compañia", default=lambda self: self.env.user.company_id)
    currency_id = fields.Many2one(
        'res.currency', default=lambda self: self.env.user.company_id.currency_id)
    st_efectivo = fields.Many2one(
        'account.bank.statement', string="Diario de efectivo", compute="compute_st_efectivo")
    saldo_apertura = fields.Monetary(
        string='Saldo de apertura', related="st_efectivo.balance_start")
    transacciones = fields.Monetary(
        string='Transacciones', related="st_efectivo.total_entry_encoding")
    saldo_teorico_cierre = fields.Monetary(
        string='Saldo teórico de cierre', related="st_efectivo.balance_end")
    saldo_cierre = fields.Monetary(
        string='Saldo cierre', related="st_efectivo.balance_end_real")
    diferencia = fields.Monetary(
        string='Diferencia', related="st_efectivo.difference")

    @api.depends('caja_id', 'statement_ids')
    def compute_st_efectivo(self):
        for i in self:
            for j in i.statement_ids:
                if j.journal_id.type == 'cash':
                    i.st_efectivo = j.id

    @api.multi
    def open_cashbox(self):
        self.ensure_one()
        context = dict(self._context)
        balance_type = context.get('balance') or 'start'
        context['bank_statement_id'] = self.st_efectivo.id
        context['balance'] = balance_type
        # context['default_pos_id'] = self.config_id.id

        action = {
            'name': 'Control de efectivo',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.bank.statement.cashbox',
            'view_id': self.env.ref('account.view_account_bnk_stmt_cashbox').id,
            'type': 'ir.actions.act_window',
            'context': context,
            'target': 'new'
        }

        cashbox_id = None
        if balance_type == 'start':
            cashbox_id = self.st_efectivo.cashbox_start_id.id
        else:
            cashbox_id = self.st_efectivo.cashbox_end_id.id
        if cashbox_id:
            action['res_id'] = cashbox_id

        return action

    def button_iniciar_sesion(self):
        self.write({'state': 'proceso'})

    def button_cerrar_sesion(self):

        facturas = self.env['account.invoice'].search(
            [('type', '=', 'out_invoice'), ('state', 'in', ['open']),
             ('date_due', '>=', fields.Date.today()),
             ('date_due', '<=', fields.Date.today()),
             ('date_invoice', '>=', fields.Date.today()),
             ('date_invoice', '<=', fields.Date.today())])

        if facturas:
            raise exceptions.ValidationError('No puede cerrar sesión, tiene facturas contado pendientes de pago.')

        if self.env.user == self.user_id or self.env.user.has_group('base.group_system'):
            for i in self.statement_ids:
                if (i != self.st_efectivo) and (i.balance_end != i.balance_end_real):
                    i.write({'balance_end_real': i.balance_end})
            self.write({'state': 'cierre', 'fecha_hora_fin': fields.Datetime.now()})
        else:
            raise exceptions.ValidationError('La sesión está asignada a otro usuario')

    def button_validar(self):
        if self.env.user == self.user_id or self.env.user.has_group('base.group_system'):
            for i in self.statement_ids:
                for j in i.line_ids:
                    for x in j.payment_id.move_line_ids.filtered(lambda z: z.debit > 0):
                        x.reconcile()
                # i.button_confirm_bank()

            for i in self.statement_ids:
                if i.journal_id.type == 'cash':
                    for j in i.line_ids:
                        if not j.journal_entry_ids:
                            move_vals = {
                                'date': i.date,
                                'ref': i.name,
                                'journal_id': i.journal_id.id,
                            }

                            move = self.env['account.move'].create(move_vals)

                            diario_diferencia = self.env['account.journal'].search([('diario_diferencia_efectivo', '=', True)])

                            if j.amount > 0 :
                                move_line_vals_debit = self.env['account.move.line'].with_context(check_move_validity=False).create({
                                    'name': j.name,
                                    'account_id': i.journal_id.id,
                                    'debit': j.amount,
                                    'credit': 0,
                                    'date_maturity': i.date,
                                    'move_id':move.id
                                })
                                move_line_vals_credit = self.env['account.move.line'].with_context(check_move_validity=False).create({
                                    'name': j.name,
                                    'account_id': diario_diferencia.default_credit_account_id.id,
                                    'debit': 0,
                                    'credit': j.amount,
                                    'date_maturity': i.date,
                                    'move_id': move.id
                                })
                                linea_a_conciliar = move_line_vals_debit
                            elif j.amount < 0:
                                move_line_vals_debit = self.env['account.move.line'].with_context(
                                    check_move_validity=False).create({
                                    'name': j.name,
                                    'account_id': diario_diferencia.default_debit_account_id.id,
                                    'credit': 0,
                                    'debit': abs(j.amount),
                                    'date_maturity': i.date,
                                    'move_id': move.id
                                })
                                move_line_vals_credit = self.env['account.move.line'].with_context(
                                        check_move_validity=False).create({
                                        'name': j.name,
                                        'account_id': i.journal_id.id,
                                        'credit': abs(j.amount),
                                        'debit': 0,
                                        'date_maturity': i.date,
                                        'move_id': move.id
                                })
                                linea_a_conciliar = move_line_vals_credit

                            move.action_post()
                            
                            j.write({'journal_entry_ids': [(4,linea_a_conciliar.id,0)]})

                            # return move
                i.button_confirm_bank()
            self.write({'state': 'done'})
            return
        else:
            raise exceptions.ValidationError('La sesión está asignada a otro usuario')

    def validar_caja_abierta(self, caja_id):
        duplicada = self.env['account.caja.session'].search(
            [('caja_id', '=', caja_id), ('state', '!=', 'done')])
        if duplicada:
            raise exceptions.ValidationError(
                'Ya existe una sesión abierta para esta caja')
        else:
            return

    def validar_sesion_unica(self, user_id):
        duplicada = self.env['account.caja.session'].search(
            [('user_id', '=', user_id), ('state', '!=', 'done')])
        if duplicada:
            raise exceptions.ValidationError(
                'Ya existe una sesión abierta para este usuario')
        else:
            return

    @api.model
    def create(self, vals):
        caja = vals.get('caja_id')
        self.validar_caja_abierta(caja)
        user = self.env.uid
        self.validar_sesion_unica(user)
        caja = self.env['account.caja'].browse(caja)
        vals['name'] = caja.sudo().sequence_id.next_by_id()
        statements = []
        for i in caja.journal_ids:
            st = {
                'journal_id': i.id,
                'name': vals.get('name'),
                'user_id': self.env.user.id,
                'company_id': self.env.user.company_id.id
            }
            statements.append((0, 0, st))
        vals['statement_ids'] = statements
        return super(AccountCajaSession, self).create(vals)

    def _notasdeCredito(self):
        for this in self:
            notasdeCredito = []

            recibos = self.env['grupo_account_payment.payment.group'].search(
                [('caja_session_id', '=', self.id), ('state', '=', 'done')])

            for recibo in recibos:
                for factura in recibo.invoice_ids:
                    for payment in factura.payment_move_line_ids:
                        if factura.type in ('out_invoice', 'in_refund'):
                            amount = sum(
                                [p.amount for p in payment.matched_debit_ids if
                                 p.debit_move_id in factura.move_id.line_ids])
                            amount_currency = sum([p.amount_currency for p in payment.matched_debit_ids if
                                                   p.debit_move_id in factura.move_id.line_ids])
                            if payment.matched_debit_ids:
                                payment_currency_id = all(
                                    [p.currency_id == payment.matched_debit_ids[0].currency_id for p in
                                     payment.matched_debit_ids]) and payment.matched_debit_ids[
                                                          0].currency_id or False
                                if payment_currency_id and payment_currency_id == factura.currency_id:
                                    amount_to_show = amount_currency
                                else:
                                    amount_to_show = payment.company_id.currency_id.with_context(
                                        date=payment.date).compute(
                                        amount, factura.currency_id)
                                if factura.partner_id.parent_id:
                                    partner_name = factura.partner_id.parent_id.name
                                else:
                                    partner_name = factura.partner_id.name
                                for nc in recibo.refund_ids:
                                    facturas = ''
                                    interes = False
                                    tipo_factura = False
                                    if payment.move_id.name == nc.number:
                                        for factura in recibo.paid_invoice_ids:
                                            facturas = facturas + factura.fake_number
                                            if factura.factura_origen_mora or factura.facturas_origen_mora:
                                                interes = True
                                            if factura.date_invoice != factura.date_due:
                                                tipo_factura = 'contado'
                                            else:
                                                tipo_factura = 'credito'
                                        notasdeCredito.append(
                                            {'tipo': 'Nota de Crédito', 'nro_documento': payment.move_id.name, 'nro_recibo':recibo.name, 'facturas':facturas,
                                             'interes':interes,
                                             'partner_id': partner_name, 'amount': amount_to_show, 'tipo_factura':tipo_factura,
                                             'date': payment.date.strftime('%d/%m/%y')})
            return notasdeCredito


class ReporteAbstract(models.AbstractModel):
    _name = 'report.account_cajas.template_reporte_sesion_caja'

    @api.model
    def _get_report_values(self, docids, data=None):
        report_name = 'account_cajas.template_reporte_sesion_caja'
        report = self.env['ir.actions.report']._get_report_from_name(report_name)
        return {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': self.env[report.model].browse(docids),
            'notasdeCredito': self.env['account.caja.session'].browse(docids)._notasdeCredito()
        }
