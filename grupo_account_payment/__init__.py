# -*- coding: utf-8 -*-

from . import controllers
from . import models
import logging
from odoo import api, SUPERUSER_ID


_logger = logging.getLogger(__name__)


def post_init_hook(cr, registry):

    env = api.Environment(cr, SUPERUSER_ID, {})
    payments = env['account.payment'].search(
        [('partner_id', '!=', False)])
    for payment in payments:
        state = payment.state
        if state in ['sent', 'reconciled', 'posted']:
            new_state = 'done'
        if state == 'cancelled':
            new_state = 'cancel'
        if state == 'draft':
            new_state = 'draft'
        name = payment.name

        _logger.info('creando grupo de pago desde pago %s' % payment.id)
        env['grupo_account_payment.payment.group'].create({
            'company_id': payment.company_id.id, 
            'partner_id': payment.partner_id.id,
            'payment_type':payment.payment_type,
            'currency_id':payment.currency_id.id,
            'fecha': payment.payment_date,
            'name': name, 
            'communication': payment.communication, 
            'payment_ids': [(4, payment.id, False)], 'state': new_state})
