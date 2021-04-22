# -*- coding: utf-8 -*-
import datetime
import uuid

from odoo import models, fields, api

from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError

class SolicitudesServicio(models.Model):
    _name = 'solicitudes.servicio'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Solicitudes de servicio'
    _order = 'name desc'

    name = fields.Char('Número', default="Borrador",
                       track_visibility='onchange', copy=False)

    fecha_solicitud = fields.Date(
        string='Fecha de solicitud', default=lambda self: fields.Date.today(), required=True, track_visibility='onchange',
        copy=False)

    fecha_estimada = fields.Date(
        string='Fecha estimada de servicio', track_visibility='onchange',
        copy=False)

    tecnico_id= fields.Many2one('res.users', string='Técnico asignado', required=False, track_visibility='onchange')

    state = fields.Selection(string='Estado', selection=[('pending','Pendiente'),(
        'draft', 'Borrador'), ('done', 'Confirmado'), ('cancel', 'Cancelado')], default='pending',
                             track_visibility='onchange')

    partner_id = fields.Many2one('res.partner', string='Cliente', required=True, track_visibility='onchange')

    partner_shipping_id = fields.Many2one('res.partner', string='Dirección', related="partner_id", readonly=0,track_visibility='onchange')

    state_id = fields.Many2one('res.country.state','Departamento del pais', related="partner_id.state_id",track_visibility='onchange')

    rubro_id = fields.Many2one('res.partner.industry','Rubro', related="partner_id.industry_id",track_visibility='onchange')

    vat = fields.Char('RUC', related="partner_id.vat",track_visibility='onchange')

    contact_id = fields.Many2one('res.partner', string='Contacto del cliente',track_visibility='onchange')

    phone = fields.Char('Teléfono', related="contact_id.phone",track_visibility='onchange')

    organismo_id = fields.Many2one('intn.organismos', string='Organismo',track_visibility='onchange')

    servicios_ids = fields.One2many('servicios.line', 'solicitud_id',string="Servicios Solicitados",track_visibility='onchange')

    detalle_servicio = fields.Html('Detalle del servicio',track_visibility='onchange')

    order_id = fields.Many2one('sale.order', string='Expediente',track_visibility='onchange')

    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env['res.company'])

    pricelist_id = fields.Many2one('product.pricelist','Lista de precios', related="partner_id.property_product_pricelist",track_visibility='onchange')

    currency_id = fields.Many2one("res.currency", related='pricelist_id.currency_id', string="Moneda", readonly=True,
                                  required=True)

    fiscal_position_id = fields.Many2one('account.fiscal.position', oldname='fiscal_position', string='Fiscal Position')

    bascula_id = fields.Many2one('intn.bascula', string='Báscula', track_visibility='onchange')


    def _default_access_token(self):
        return uuid.uuid4().hex


    access_url = fields.Char('URL del portal de cliente', compute="_compute_access_url")
    access_token = fields.Char('Token de seguridad', default=_default_access_token)

    @api.multi
    def _get_report_base_filename(self):
        self.ensure_one()
        return '%s %s' % ('Solicitud de Servicio', self.name)

    def _compute_access_url(self):
        # super(SolicitudesServicio, self)._compute_access_url()
        for solicitud in self:
            solicitud.access_url = '/my/solicitudes/%s' % (solicitud.id)

    def _portal_ensure_token(self):
        """ Get the current record access token """
        if not self.access_token:
            # we use a `write` to force the cache clearing otherwise `return self.access_token` will return False
            self.sudo().write({'access_token': str(uuid.uuid4())})
        return self.access_token

    @api.multi
    def get_portal_url(self, suffix=None, report_type=None, download=None, query_string=None, anchor=None):
        self.ensure_one()
        url = self.access_url + '%s?access_token=%s%s%s%s%s' % (
            suffix if suffix else '',
            self._portal_ensure_token(),
            '&report_type=%s' % report_type if report_type else '',
            '&download=true' if download else '',
            query_string if query_string else '',
            '#%s' % anchor if anchor else ''
        )
        return url

    @api.multi
    @api.onchange('partner_shipping_id', 'partner_id')
    def onchange_partner_shipping_id(self):
        """
        Trigger the change of fiscal position when the shipping address is modified.
        """
        self.fiscal_position_id = self.env['account.fiscal.position'].get_fiscal_position(self.partner_id.id,
                                                                                          self.partner_shipping_id.id)
        return {}


    def button_draft(self):
        # if not self.tecnico_id:
        #     raise ValidationError(
        #         'Debe asignar un técnico antes de cambiar de estado la Solicitud de Servicio')
        # if not self.fecha_estimada:
        #     raise ValidationError(
        #         'Debe cargar una fecha estimada antes de cambiar de estado la Solicitud de Servicio')
        self.write({'state': 'draft'})

    @api.model
    def create(self, vals):
        r = super(SolicitudesServicio, self).create(vals)
        for i in r:
            organismo = ''
            for servicio in i.servicios_ids:
                organismo = servicio.organismo_id
            new_name = self.sudo().env['ir.sequence'].next_by_code('seq_solicitudes_servicio')
            i.write({'name':new_name,'organismo_id':organismo})
            reg = {
                'res_id': i.id,
                'res_model': 'solicitudes.servicio',
                'partner_id': i.partner_id.id
            }
            follower_id = self.env['mail.followers'].create(reg)
        return r


    def button_confirmar(self):
        self.write({'state': 'done'})


    def button_cancelar(self):
        self.write({'state': 'cancel'})

    def button_expediente(self):
        lines = []
        for line in self.servicios_ids:
            linea = {
                'customer_lead': 0,
                'product_id': line.product_id.id,
                'name': line.name,
                'order_id': self.order_id,
                'price_unit': line.price_unit,
                'product_uom_qty': line.product_uom_qty,
                'tax_id': [(6, 0, line.tax_id.ids)],
            }
            lines.append((0, 0, linea))
        values = {
            'partner_id': self.partner_id.id,
            'partner_shipping_id':self.partner_shipping_id.id,
            'partner_invoice_id':self.partner_id.id,
            'date_order':datetime.datetime.now(),
            'fecha':datetime.datetime.now(),
            'fecha_estimada': self.fecha_estimada or False,
            #'tecnico_id': self.tecnico_id or False,
            'origin': self.name,
            'solicitud_id': self.id
        }

        order = self.env['sale.order'].create(
            values)
        order.write({'order_line': lines})
        self.update({'order_id': order.id})


class ServiciosLine(models.Model):
    _name = 'servicios.line'

    solicitud_id = fields.Many2one('solicitudes.servicio', string='Solicitud de Servicios', required=True, ondelete='cascade', index=True,
                               copy=False)

    currency_id = fields.Many2one("res.currency", related='solicitud_id.currency_id', string="Moneda", readonly=True,
                                  required=True)

    name = fields.Text(string='Descripción', required=True)

    product_id = fields.Many2one('product.product', string='Servicio', domain=[('aparece_solicitudes_servicio', '=', True)],
                                 change_default=True, ondelete='restrict')
    price_unit = fields.Float('Precio Unitario', required=True, digits=dp.get_precision('Product Price'), default=0.0)

    tax_id = fields.Many2many('account.tax', string='Impuestos',
                              domain=['|', ('active', '=', False), ('active', '=', True)])

    price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', readonly=True, store=True)
    price_tax = fields.Float(compute='_compute_amount', string='Total Impuestos', readonly=True, store=True)
    price_total = fields.Monetary(compute='_compute_amount', string='Total', readonly=True, store=True)

    product_uom_qty = fields.Float(string='Cantidad', digits=dp.get_precision('Product Unit of Measure'),
                                   required=True, default=1.0)
    product_uom = fields.Many2one('uom.uom', string='Unidad de medida',related="product_id.uom_id")


    @api.depends('product_id')
    @api.onchange('product_id')
    def onChangeProduct(self):
        self._compute_tax_id()
        price_list = self.env['product.pricelist.item'].search([('pricelist_id', '=', self.solicitud_id.pricelist_id.id)])
        price_list_item = price_list.filtered(lambda x: x.product_id == self.product_id)
        if price_list_item:
            self.price_unit = price_list_item.fixed_price
        else:
            self.price_unit = self.product_id.list_price
        self.name = self.product_id.product_tmpl_id.name + self.product_id.product_tmpl_id.determinacion

    @api.multi
    def _compute_tax_id(self):
        for line in self:
            fpos = line.solicitud_id.fiscal_position_id or line.solicitud_id.partner_id.property_account_position_id
            taxes = line.product_id.taxes_id.filtered(lambda r: not line.solicitud_id.company_id or r.company_id == line.solicitud_id.company_id)
            line.tax_id = fpos.map_tax(taxes, line.product_id, line.solicitud_id.partner_shipping_id) if fpos else taxes

    @api.depends('product_uom_qty', 'price_unit', 'tax_id')
    def _compute_amount(self):
        self._compute_tax_id()
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit
            taxes = line.tax_id.compute_all(price, line.solicitud_id.currency_id, line.product_uom_qty,
                                            product=line.product_id, partner=line.solicitud_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })