# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.addons.payment.controllers.portal import PaymentProcessing
from odoo.exceptions import AccessError, MissingError
from odoo.http import request

class SaleOrderPortal(CustomerPortal):

    @http.route(['/my/invoices/<int:invoice_id>'], type='http', auth="public", website=True)
    def portal_my_invoice_detail(self, invoice_id, access_token=None, report_type=None, download=False, **kw):
        try:
            invoice_sudo = self._document_check_access('account.invoice', invoice_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=invoice_sudo, report_type=report_type, report_ref='factura_autoimpresor.factura_report_action',
                                     download=download)

        values = self._invoice_get_page_view_values(invoice_sudo, access_token, **kw)
        PaymentProcessing.remove_payment_transaction(invoice_sudo.transaction_ids)
        return request.render("account.portal_invoice_page", values)


#     @http.route('/sale_order_portal/sale_order_portal/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_order_portal/sale_order_portal/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_order_portal.listing', {
#             'root': '/sale_order_portal/sale_order_portal',
#             'objects': http.request.env['sale_order_portal.sale_order_portal'].search([]),
#         })

#     @http.route('/sale_order_portal/sale_order_portal/objects/<model("sale_order_portal.sale_order_portal"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_order_portal.object', {
#             'object': obj
#         })