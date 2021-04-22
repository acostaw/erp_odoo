from odoo import fields, models, api


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    diario_caja = fields.Boolean('Diario de caja', default=False,
        help="Marque ésta casilla para que diario pueda ser usado en cajas")

    diario_diferencia_efectivo = fields.Boolean('Diario de diferencia de Efectivo', default=False,
                                 help="Marque ésta casilla para que diario pueda ser usado en cajas")

