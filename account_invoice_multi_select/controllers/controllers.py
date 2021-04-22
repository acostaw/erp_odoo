# -*- coding: utf-8 -*-
from odoo import http

# class AccountInvoiceMultiSelect(http.Controller):
#     @http.route('/account_invoice_multi_select/account_invoice_multi_select/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_invoice_multi_select/account_invoice_multi_select/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_invoice_multi_select.listing', {
#             'root': '/account_invoice_multi_select/account_invoice_multi_select',
#             'objects': http.request.env['account_invoice_multi_select.account_invoice_multi_select'].search([]),
#         })

#     @http.route('/account_invoice_multi_select/account_invoice_multi_select/objects/<model("account_invoice_multi_select.account_invoice_multi_select"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_invoice_multi_select.object', {
#             'object': obj
#         })