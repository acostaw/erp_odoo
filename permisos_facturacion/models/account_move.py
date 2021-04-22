# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import datetime,math,locale
from odoo.exceptions import ValidationError


class AccountPartialReconcile(models.Model):
    _inherit = 'account.partial.reconcile'

    @api.multi
    def unlink(self):
        for i in self:
            if not self.env.user.has_group('permisos_facturacion.group_romper_conciliaciones'):
                raise exceptions.ValidationError('No tiene permisos para romper conciliaciones. Contacte con su administrador')
            return super(AccountPartialReconcile, self).unlink()