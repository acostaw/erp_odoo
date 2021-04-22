# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.payment.controllers.portal import PaymentProcessing
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager
from odoo.osv import expression
from datetime import date
import json


class CustomerPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()

        session_uid = request.session.uid
        if session_uid:
            partner = request.env['res.users'].browse(request.session.uid).partner_id

        SolicitudesServicio = request.env['solicitudes.servicio']
        solicitud_count = SolicitudesServicio.search_count([
            ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
            ('state', 'in', ['pending', 'draft', 'done', 'cancel'])
        ])

        values.update({
            'solicitud_count': solicitud_count,
        })

        return values

    @http.route(['/my/solicitudes', '/my/solicitudes/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_solicitudes(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        SolicitudesServicio = request.env['solicitudes.servicio']

        domain = [
            ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
            ('state', 'in', ['pending', 'draft', 'done', 'cancel'])
        ]

        searchbar_sortings = {
            'date': {'label': _('Fecha Solicitud'), 'order': 'fecha_solicitud desc'},
            'name': {'label': _('Referencia'), 'order': 'name'},
            'stage': {'label': _('Estado'), 'order': 'state'},
        }

        # default sortby order
        if not sortby:
            sortby = 'date'
        sort_order = searchbar_sortings[sortby]['order']

        archive_groups = self._get_archive_groups('solicitudes.servicio', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # count for pager
        quotation_count = SolicitudesServicio.search_count(domain)
        # make pager
        pager = portal_pager(
            url="/my/solicitudes",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=quotation_count,
            page=page,
            step=self._items_per_page
        )
        # search the count to display, according to the pager data
        quotations = SolicitudesServicio.search(domain, order=sort_order, limit=self._items_per_page,
                                                offset=pager['offset'])
        request.session['my_solicitudes_history'] = quotations.ids[:100]

        values.update({
            'date': date_begin,
            'quotations': quotations.sudo(),
            'page_name': 'solicitud',
            'pager': pager,
            'archive_groups': archive_groups,
            'default_url': '/my/solicitudes',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })

        return request.render("solicitudes_servicio.portal_my_solicitudes", values)

    @http.route(['/my/solicitudes/<int:solicitud_id>'], type='http', auth="public", website=True)
    def portal_solicitud_page(self, solicitud_id, report_type=None, access_token=None, message=False, download=False,
                              **kw):
        try:
            solicitud_sudo = self._document_check_access('solicitudes.servicio', solicitud_id,
                                                         access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=solicitud_sudo, report_type=report_type,
                                     report_ref='solicitudes_servicio.reporte_solicitud', download=download)

        # use sudo to allow accessing/viewing orders for public user
        # only if he knows the private token
        now = fields.Date.today()

        # Log only once a day
        if solicitud_sudo and request.session.get(
                'view_quote_%s' % solicitud_sudo.id) != now and request.env.user.share and access_token:
            request.session['view_quote_%s' % solicitud_sudo.id] = now
            body = _('Solicitud vista por el cliente')
            _message_post_helper(res_model='solicitudes.servicio', res_id=solicitud_sudo.id, message=body,
                                 token=solicitud_sudo.access_token, message_type='notification', subtype="mail.mt_note",
                                 partner_ids=solicitud_sudo.partner_id.user_id.sudo().partner_id.ids)

        values = {
            'solicitud_servicio': solicitud_sudo,
            'message': message,
            'token': access_token,
            'bootstrap_formatting': True,
            'partner_id': solicitud_sudo.partner_id.id,
            'report_type': 'html',
            'page_name': 'solicitud',
        }
        if solicitud_sudo.company_id:
            values['res_company'] = solicitud_sudo.company_id

        if solicitud_sudo.state in ('draft', 'sent', 'cancel'):
            history = request.session.get('my_solicitudes_history', [])
        else:
            history = request.session.get('my_solicitudes_history', [])
        values.update(get_records_pager(history, solicitud_sudo))

        return request.render('solicitudes_servicio.solicitud_servicio_portal_template', values)

    @http.route(['/new/solicitud'], type='http', auth="user", website=True)
    def portal_new_solicitud(self, **kw):
        session_uid = request.session.uid
        if session_uid:
            partner = request.env['res.users'].browse(request.session.uid).partner_id
            sucursales = partner.child_ids
        price_list = http.request.env['product.pricelist.item'].sudo().search(
            [('pricelist_id', '=', partner.property_product_pricelist.id)])
        search_domain = [('sale_ok', '=', True), ('aparece_solicitudes_servicio', '=', True)]
        servicios = request.env['product.product'].search(search_domain)
        organismos = request.env['intn.organismos'].sudo().search(
            [('active', '=', True)])
        fecha_actual = date.today().strftime("%d/%m/%Y")

        basculas = []

        if partner.bascula_ids:
            basculas = partner.bascula_ids

        return http.request.render('solicitudes_servicio.nueva_solicitud_servicio',
                                   {'servicios': servicios, 'organismos': organismos, 'price_list': price_list,
                                    'fecha_actual': fecha_actual, 'partner': partner,'page_name':'solicitud','sucursales':sucursales,'basculas':basculas})

    @http.route('/save/solicitud', auth='user', website=True, )
    def get_partners(self, **kw):
        if int(kw['sucursal']) != 0:
            partner= kw['sucursal']
        else:
            partner = kw['partner']

        values = {
            'partner_id': partner,
            'fecha_solicitud': date.today(),
            'detalle_servicio': kw['detalle_servicio'],
            'bascula_id': kw['bascula'],
        }
        solicitud = request.env['solicitudes.servicio'].sudo().create(values)

        search_domain = [('id', '=', kw['servicio'])]
        servicio = request.env['product.product'].search(search_domain)
        organismo = servicio.organismo_id
        list_price = servicio.list_price

        lines = []

        linea = {
            'solicitud_id': solicitud.id,
            'product_id': kw['servicio'],
            'name': servicio.name + servicio.determinacion,
            'product_uom_qty':kw['cantidad'],
            'price_unit':list_price,
        }

        lines.append((0, 0, linea))

        solicitud.sudo().write({'servicios_ids':lines,'organismo_id':organismo.id})

        return http.request.render('solicitudes_servicio.solicitud_creada',
                                   {'solicitud': solicitud,'page_name':'solicitud'})

    @http.route(['/get-basculas/<int:partner_id>'], type='http', auth="public", website=True)
    def get_basculas(self, partner_id, **kw):

        if partner_id != 0:
            partner = request.env['res.partner'].browse(partner_id)
        else:
            partner = request.env['res.users'].browse(request.session.uid).partner_id

        basculas_a_enviar = []
        if partner:
            if partner.bascula_ids:
                for bascula in partner.bascula_ids:
                    p = {'id': bascula.id, 'name': bascula.name}

                    basculas_a_enviar.append(p)

        return json.dumps(basculas_a_enviar)