# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager
import json


class CustomerPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()

        session_uid = request.session.uid
        if session_uid:
            partner = request.env['res.users'].browse(request.session.uid).partner_id

        partner_bascula = partner.filtered(lambda x: x.partner_latitude != False and x.partner_longitude != False and x.bascula_ids != False)

        partners_a_enviar = []

        if partner_bascula:
            partners_a_enviar.append(partner_bascula)

        if partner_bascula.child_ids:
            for child in partner_bascula.child_ids:
                if child.partner_latitude != False and child.partner_longitude != False and child.bascula_ids:
                    partners_a_enviar.append(child)

        values.update({
            'basculas_count': len(partners_a_enviar),
        })

        return values

    @http.route(['/my/basculas'], type='http', auth="user", website=True)
    def bascula(self):
        session_uid = request.session.uid
        if session_uid:
            partner = request.env['res.users'].browse(request.session.uid).partner_id

        partner_bascula = partner.filtered(
            lambda x: x.partner_latitude != False and x.partner_longitude != False and x.bascula_ids != False)

        mensaje = False

        if not partner_bascula:
            mensaje = 'No tiene basculas que ver'
        return request.render("intn_informe_bascula_web.listado_basculas_partner", {'mensaje': mensaje, 'basculas':partner_bascula})

    @http.route('/basculas_cliente', auth='user', website=True, type='http')
    def basculas_cliente(self):

        session_uid = request.session.uid
        if session_uid:
            partner = request.env['res.users'].browse(request.session.uid).partner_id

        partner_bascula = partner.filtered(lambda x: x.partner_latitude != False and x.partner_longitude != False and x.bascula_ids != False)

        partners_a_enviar = []

        p = {'id': partner_bascula.id, 'name': partner_bascula.display_name, 'basculas': partner_bascula.basculas,
                 'partner_lat': partner_bascula.partner_latitude, 'partner_lng': partner_bascula.partner_longitude}
        partners_a_enviar.append(p)
        if partner_bascula.child_ids:
            for child in partner_bascula.child_ids:
                if child.partner_latitude != False and child.partner_longitude != False and child.bascula_ids:
                    p = {'id': child.id, 'name': child.display_name,
                         'basculas': child.basculas,
                         'partner_lat': child.partner_latitude,
                         'partner_lng': child.partner_longitude}
                    partners_a_enviar.append(p)

        return json.dumps(partners_a_enviar)