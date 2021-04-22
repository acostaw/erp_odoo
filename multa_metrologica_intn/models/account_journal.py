from odoo import fields, models, api


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    diario_multa = fields.Boolean('Diario de Multas Metrologicas', default=False,
        help="Marque ésta casilla si este diaria corresponde al diario de Multas Metrologicas")