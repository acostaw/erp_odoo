from odoo import fields, api, models


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    timbrados_ids = fields.One2many(
        'interfaces_timbrado.timbrado', 'journal_id', string="Timbrados")
    max_lineas = fields.Integer(
        string="Cantidad máxima de líneas imprimibles de la factura", default=0)
    diario_notas_credito = fields.Boolean(
        string="Diario de notas de credito", default=False)
