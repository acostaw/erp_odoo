# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager

class IntnInformeBasculaWeb(http.Controller):
    @http.route('/listado-basculas', auth='public', website='True')
    def index(self, **kw):
        partners = http.request.env['res.partner'].sudo().search(
            [('bascula_ids', '!=', False)])
        departamentos = http.request.env['res.country.state'].sudo().search(
            [('departamento_paraguay', '=', True)], order="code desc")
        return request.render("intn_informe_bascula_web.listado_basculas",{'partners':partners,'departamentos':departamentos})

    @http.route('/partners', auth='public', website=True, type='http')
    def partners(self):
        search_domain = [('partner_latitude', '!=', False),
                         ('partner_longitude', '!=', False),
                         ('bascula_ids', '!=', False)]

        partners = http.request.env['res.partner'].sudo().search(search_domain)

        partners_a_enviar = []

        for i in partners:
            p = {'id': i.id, 'name': i.display_name, 'basculas': i.basculas_publico,
                 'partner_lat': i.partner_latitude, 'partner_lng': i.partner_longitude}
            partners_a_enviar.append(p)

        return json.dumps(partners_a_enviar)

    @http.route('/search-bascula', auth='public', website=True, )
    def get_bascula(self, searchTerm=None,dpto=None,ciudad=None,estado=None,**kwargs):
        search_domain = [('partner_latitude','!=',False),('partner_latitude','!=',False),('bascula_ids','!=',False)]

        if ciudad:
            search_domain.append(('city', 'ilike', ciudad))

        if dpto != '0':
            search_domain.append(('state_id', '=', int(dpto)))

        partners = http.request.env['res.partner'].sudo().search(search_domain)

        if searchTerm:
            partners = partners.filtered(lambda x: searchTerm.upper() in x.display_name.upper()
                                               or searchTerm.upper() in x.vat.upper()
                                        )
        if estado != 0:
            partners = partners.filtered(lambda x: estado.upper() in x.basculas.upper())


        partners_a_enviar = []


        for i in partners:
            p = {'id': i.id, 'name': i.display_name, 'basculas': i.basculas_publico,
                 'partner_lat': i.partner_latitude, 'partner_lng': i.partner_longitude}
            partners_a_enviar.append(p)

        return json.dumps(partners_a_enviar)

