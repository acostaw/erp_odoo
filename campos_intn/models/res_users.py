# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPUsers(models.Model):
    _inherit = "res.users"

    notification_type = fields.Selection(default='inbox')
