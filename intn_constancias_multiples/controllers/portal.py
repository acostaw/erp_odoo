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


class CustomerPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()

        session_uid = request.session.uid
        if session_uid:
            partner = request.env['res.users'].browse(request.session.uid).partner_id

        ConstanciasMultiples = request.env['constancias.multiples']
        constancias_count = ConstanciasMultiples.search_count([
            ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
            ('state', 'in', [ 'draft', 'done', 'cancel'])
        ])

        values.update({
            'constancias_count': constancias_count,
        })

        return values

    @http.route(['/my/constancias', '/my/constancias/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_constancias(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        ConstanciasMultiples = request.env['constancias.multiples']

        domain = [
            ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
            ('state', 'in', ['draft', 'done', 'cancel'])
        ]

        searchbar_sortings = {
            'date': {'label': _('Fecha de Creación'), 'order': 'create_date desc'},
            'name': {'label': _('Referencia'), 'order': 'name'},
            'stage': {'label': _('Estado'), 'order': 'state'},
        }

        # default sortby order
        if not sortby:
            sortby = 'date'
        sort_order = searchbar_sortings[sortby]['order']

        archive_groups = self._get_archive_groups('constancias.multiples', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # count for pager
        quotation_count = ConstanciasMultiples.search_count(domain)
        # make pager
        pager = portal_pager(
            url="/my/constancias",
            url_args={'date_begin': date_begin, 'date_end': date_end,'sortby': sortby},
            total=quotation_count,
            page=page,
            step=self._items_per_page
        )
        # search the count to display, according to the pager data
        constancias = ConstanciasMultiples.search(domain, order=sort_order, limit=self._items_per_page,
                                                offset=pager['offset'])
        request.session['my_constancias_history'] = constancias.ids[:100]

        values.update({
            'date': date_begin,
            'constancias': constancias.sudo(),
            'page_name': 'constancia',
            'pager': pager,
            'archive_groups': archive_groups,
            'default_url': '/my/constancias',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })

        return request.render("intn_constancias_multiples.portal_my_constancias", values)

    @http.route(['/my/constancias/<int:constancia_id>'], type='http', auth="public", website=True)
    def portal_constancia_page(self, constancia_id, report_type=None, access_token=None, message=False, download=False,
                              **kw):
        try:
            constancia_sudo = self._document_check_access('constancias.multiples', constancia_id,
                                                         access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=constancia_sudo, report_type=report_type,
                                     report_ref='intn_constancias_multiples.reporte_constancia', download=download)

        # use sudo to allow accessing/viewing orders for public user
        # only if he knows the private token
        now = fields.Date.today()

        # Log only once a day
        if constancia_sudo and request.session.get(
                'view_quote_%s' % constancia_sudo.id) != now and request.env.user.share and access_token:
            request.session['view_quote_%s' % constancia_sudo.id] = now
            body = _('Constancia vista por el cliente')
            _message_post_helper(res_model='constancias.multiples', res_id=constancia_sudo.id, message=body,
                                 token=constancia_sudo.access_token, message_type='notification', subtype="mail.mt_note",
                                 partner_ids=constancia_sudo.partner_id.user_id.sudo().partner_id.ids)

        values = {
            'constancias_multiples': constancia_sudo,
            'message': message,
            'token': access_token,
            'bootstrap_formatting': True,
            'partner_id': constancia_sudo.partner_id.id,
            'report_type': 'html',
            'page_name': 'constancia',
        }
        if constancia_sudo.company_id:
            values['res_company'] = constancia_sudo.company_id

        if constancia_sudo.state in ('draft', 'done', 'cancel'):
            history = request.session.get('my_constancias_history', [])
        else:
            history = request.session.get('my_constancias_history', [])
        values.update(get_records_pager(history, constancia_sudo))

        return request.render('intn_constancias_multiples.constancias_multiples_portal_template', values)
