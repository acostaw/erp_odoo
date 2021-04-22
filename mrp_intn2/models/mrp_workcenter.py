from odoo import fields, api, models, exceptions


class mrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'
    user_ids = fields.Many2many('res.users',
                                ondelete='cascade', string="Usuarios")
