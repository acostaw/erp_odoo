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
import hashlib


class CustomerPortal(CustomerPortal):


    @http.route('/my/informes/bascula/check', auth='public', website=True)
    def index(self,id,token):
        if token==self.genera_token(str(id)):
            informe=http.request.env['informes.bascula'].sudo().search([('id','=',int(id)),('state','=','done')])
            return http.request.render('intn_informe_bascula.online_informe_bascula',{'informe':informe})
        else:
            return http.request.render('intn_informe_bascula.token_invalido')

    def genera_token(self,id_informe):
        palabra=id_informe+"amakakeruriunohirameki"
        return hashlib.sha256(bytes(palabra,'utf-8')).hexdigest()


    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()

        session_uid = request.session.uid
        if session_uid:
            partner = request.env['res.users'].browse(request.session.uid).partner_id

        InformesBascula = request.env['informes.bascula']
        bascula_count = InformesBascula.search_count([
            ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
            ('state', 'in', [ 'draft', 'done', 'cancel'])
        ])

        values.update({
            'bascula_count': bascula_count,
        })

        return values

    @http.route(['/my/informes/bascula', '/my/informes/bascula/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_constancias(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        InformesBascula = request.env['informes.bascula']

        domain = [
            ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
            ('state', 'in', ['draft', 'done', 'cancel'])
        ]

        searchbar_sortings = {
            'date': {'label': _('Fecha'), 'order': 'fecha desc'},
            'name': {'label': _('Referencia'), 'order': 'name'},
            'stage': {'label': _('Estado'), 'order': 'state'},
        }

        # default sortby order
        if not sortby:
            sortby = 'date'
        sort_order = searchbar_sortings[sortby]['order']

        archive_groups = self._get_archive_groups('informes.bascula', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # count for pager
        bascula_count = InformesBascula.search_count(domain)
        # make pager
        pager = portal_pager(
            url="/my/informes/bascula",
            url_args={'date_begin': date_begin, 'date_end': date_end,'sortby': sortby},
            total=bascula_count,
            page=page,
            step=self._items_per_page
        )
        # search the count to display, according to the pager data
        informes_bascula = InformesBascula.search(domain, order=sort_order, limit=self._items_per_page,
                                                  offset=pager['offset'])
        request.session['my_informes_bascula_history'] = informes_bascula.ids[:100]

        values.update({
            'date': date_begin,
            'informes_bascula': informes_bascula.sudo(),
            'page_name': 'informes_bascula',
            'pager': pager,
            'archive_groups': archive_groups,
            'default_url': '/my/informes/bascula',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })

        return request.render("intn_informe_bascula.portal_my_informes_bascula", values)

    @http.route(['/my/informes/bascula/<int:informe_bascula_id>'], type='http', auth="public", website=True)
    def portal_constancia_page(self, informe_bascula_id, report_type=None, access_token=None, message=False, download=False,
                               **kw):
        try:
            informe_bascula_sudo = self._document_check_access('informes.bascula', informe_bascula_id,
                                                               access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=informe_bascula_sudo, report_type=report_type,
                                     report_ref='intn_informe_bascula.reporte_bascula', download=download)

        # use sudo to allow accessing/viewing orders for public user
        # only if he knows the private token
        now = fields.Date.today()

        # Log only once a day
        if informe_bascula_sudo and request.session.get(
                'view_quote_%s' % informe_bascula_sudo.id) != now and request.env.user.share and access_token:
            request.session['view_quote_%s' % informe_bascula_sudo.id] = now
            body = _('Informe de Verificación de IPNA - Bascula vista por el cliente')
            _message_post_helper(res_model='informes.bascula', res_id=informe_bascula_sudo.id, message=body,
                                 token=informe_bascula_sudo.access_token, message_type='notification', subtype="mail.mt_note",
                                 partner_ids=informe_bascula_sudo.partner_id.user_id.sudo().partner_id.ids)

        values = {
            'informes_bascula': informe_bascula_sudo,
            'message': message,
            'token': access_token,
            'bootstrap_formatting': True,
            'partner_id': informe_bascula_sudo.partner_id.id,
            'report_type': 'html',
            'page_name': 'informes_bascula',
        }
        if informe_bascula_sudo.company_id:
            values['res_company'] = informe_bascula_sudo.company_id

        if informe_bascula_sudo.state in ('draft', 'done', 'cancel'):
            history = request.session.get('my_informes_bascula_history', [])
        else:
            history = request.session.get('my_informes_bascula_history', [])
        values.update(get_records_pager(history, informe_bascula_sudo))

        return request.render('intn_informe_bascula.informes_bascula_portal_template', values)

    @http.route('/save/feedback', auth='user', website=True, )
    def save_feedback(self, **kw):
        rating = kw['ratingForm']
        feedback = kw['feedback']

        search_domain = [('id', '=', kw['informe'])]
        informe = request.env['informes.bascula'].search(search_domain)

        informe.sudo().write({'feedback': feedback, 'calificacion': rating})

        return
