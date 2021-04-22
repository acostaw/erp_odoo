from odoo import fields, api, models


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    facturas_sueltas = fields.Boolean(string="Permitir crear facturas sueltas", default=False)