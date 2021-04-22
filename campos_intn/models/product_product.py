# -*- coding: utf-8 -*-

from odoo import models, fields, api


class productName(models.Model):
    _inherit = "product.product"

    @api.multi
    def name_get(self):
        res = super(productName, self).name_get()
        data = []
        for this in self:
            display_value = this.name
            if this.determinacion:
                display_value += ' - ' + this.determinacion
            data.append((this.id, display_value))
        return data