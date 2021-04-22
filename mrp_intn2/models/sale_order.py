# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    numero_informe = fields.Char(string="Numero de Informe")
    pago_exonerado_manual=fields.Boolean(default=False,copy=False, track_visibility='onchange')
    # def get_workscenter(self):
    #     workcenters=[]
    #     for i in self.env['mrp.workcenter'].search[()]:
    #         print(i.user_ids)
    #         if user in i.user_ids:
    #             workcenters.append(i.id)
    #
    #     return workcenters

    def action_confirm(self):
        for i in self:
            res = super(SaleOrder, i).action_confirm()
            if i.pago_exonerado:
                mrps = self.env['mrp.production'].search(
                    [('state', '=', 'confirmed'), ('origin', '=', i.name)])
                for m in mrps:
                    m.write({'name': i.name+'/'+m.name})
                    m.button_plan()
            return res

    def marcar_pago_exonerado_manual(self):
        for i in self:
            i.update({'pago_exonerado_manual':True})

    def _pago_exonerado(self):
        for i in self:
            super(SaleOrder,i)._pago_exonerado()
            if i.pago_exonerado_manual:
                i.pago_exonerado=True
            return
