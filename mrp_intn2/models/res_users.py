# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = "res.users"

    # def get_workscenter(self):
    #     workcenters=[]
    #     for i in self.env['mrp.workcenter'].search[()]:
    #         print(i.user_ids)
    #         if user in i.user_ids:
    #             workcenters.append(i.id)
    #
    #     return workcenters


