# -*- coding: utf-8 -*-
import itertools

from odoo import models, api, fields, exceptions
from lxml import etree
from odoo.exceptions import ValidationError
from openerp.osv.orm import setup_modifiers
import re
import uuid


class ConstanciasMultiples(models.Model):
    _name = 'constancias.multiples'
    _description = 'Constancias Multiples'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'
    #     pantilla_constancia_id = fields.Many2one('plantila.constancias')

    name = fields.Char('Número', default="Borrador",
                       track_visibility='onchange', copy=False, required=True)
    order_id = fields.Many2one(
        'sale.order', string="Expediente", required=True)

    partner_id = fields.Many2one('res.partner', string="Solicitante", related="order_id.partner_id", store=True)

    line_ids = fields.One2many(
        'constancia.lineas', 'constancia_multiple_id', string='Lineas', copy=True)

    tipo_constancia_id = fields.Many2one('tipo.constancias', string="Tipo de Constancia", required=True)

    embed_code = fields.Char(compute="setDefaultID")

    cuerpo = fields.Html(string="Cuerpo de la constancia", compute="computeContenido")
    cuerpo_original = fields.Html(string="Cuerpo de la constancia", related="tipo_constancia_id.cuerpo")

    state = fields.Selection(string='Estado', selection=[(
        'draft', 'Borrador'), ('done', 'Confirmado'), ('cancel', 'Cancelado')], default='draft',
                             track_visibility='onchange')

    user_id = fields.Many2one('res.users', 'Usuario',
                              default=lambda self: self.env.user)

    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env['res.company'])

    def _default_access_token(self):
        return uuid.uuid4().hex


    access_url = fields.Char('URL del portal de cliente', compute="_compute_access_url")
    access_token = fields.Char('Token de seguridad', default=_default_access_token)

    @api.multi
    def _get_report_base_filename(self):
        self.ensure_one()
        return '%s %s' % ('Constancia', self.name)

    def _compute_access_url(self):
        # super(SolicitudesServicio, self)._compute_access_url()
        for constancia in self:
            constancia.access_url = '/my/constancias/%s' % (constancia.id)

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

    @api.onchange('order_id')
    @api.depends('order_id')
    def onchangeorder(self):
        for this in self:
            this.update({'line_ids': [(5, 0, 0)]})
            if this.order_id:
                # this.solicitante_id = this.order_id.partner_id.id
                # this.fecha_expediente = this.order_id.confirmation_date
                lines = []
                product_count = 0
                for line in this.order_id.order_line:
                    for product in line.product_id:
                        product_count += 1
                        if product_count > 1:
                            raise ValidationError(
                                'El expediente seleccionado cuenta con más de un producto')
                        else:
                            # this.departamento_id = product.departamento_id
                            d = {
                                'product_id': product.id,
                            }
                            lines.append((0, 0, d))
                this.update({'line_ids': lines})

    def button_confirmar(self):
        for i in self:
            i.asigna_nombre()
            i.write({'state': 'done', 'fecha_informe': fields.Datetime.now()})

    def button_cancelar(self):
        for i in self:
            if i.order_id:
                factura = self.env['account.invoice'].search([('origin', '=', i.order_id.name)])
                if factura:
                    factura.action_invoice_cancel()
                i.order_id.action_cancel()
            i.write({'state': 'cancel'})

    def button_draft(self):
        for i in self:
            i.write({'state': 'draft'})


    @api.onchange('tipo_constancia_id')
    def setDefaultID(self):
        self.embed_code = self.tipo_constancia_id.id

    def getFields(self,params):
        plantilla = self.env['tipo.constancias'].search([('id', '=', params)]).plantilla_id
        campos1 = plantilla.mapped('fields_ids').sorted(key=lambda r: r.sequence).mapped('fields_id').mapped('name')
        campos2 = plantilla.mapped('fields_ids').sorted(key=lambda r: r.sequence).mapped('fields_id').mapped('field_description')
        campos= campos1 + campos2
        return campos


    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(ConstanciasMultiples, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        campos = self.env['ir.model.fields'].search([('model', '=', 'constancias.multiples'), (
        'name', 'not in', ['embed_code', 'order_id', 'tipo_constancia_id','state','line_ids','partner_id','user_id','access_url','access_token','company_id'])])
        sep = None
        i = 0
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            for node in doc.xpath("//group[@name='grupo']"):
                for cam in campos:
                    # if i % 2 == 0:
                    #     sep = etree.Element(
                    #         'group', {
                    #             'string': '',
                    #         })
                    #     node.insert(i, sep)
                    elem = etree.Element(
                        'field', {
                            'name': cam.name,
                            'string': cam.field_description,
                        })
                    # if sep is not None:
                    #     sep.append(elem)
                    # else:
                    node.append(elem)
                    # elem.set('class', 'not_display')
                    elem.set('invisible', '1')
                    elem.set('readonly',"[('state','!=','draft')]")
                    setup_modifiers(elem, res['fields'])
                    i = i + 1

            res['arch'] = etree.tostring(doc)
        return res

    def genera_secuencia(self):
        for this in self:
            count = 0
            for line in this.order_id.order_line:
                for product in line.product_id:
                    if product.secuencia_constancia:
                        code = product.secuencia_constancia
                        seq = code.next_by_id()
                        return seq
                    else:
                        raise ValidationError(
                            'Debe asignar el codigo de secuencia al producto')

    def asigna_nombre(self):
        for i in self:
            if self.name and self.name == 'Borrador':
                new_name = i.genera_secuencia()
                i.write({'name': new_name})
            else:
                return



    @api.model_create_multi
    @api.returns('self', lambda value: value.id)
    def create(self, vals_list):
        res = super(ConstanciasMultiples, self).create(vals_list)
        for i in res:
            reg = {
                'res_id': i.id,
                'res_model': 'constancias.multiples',
                'partner_id': i.partner_id.id
            }
            follower_id = self.env['mail.followers'].create(reg)
        return res

    @api.depends('tipo_constancia_id')
    @api.depends('cuerpo')
    def computeContenido(self):
        for this in self:
            contenido = this.tipo_constancia_id.cuerpo
            if contenido:
                print(contenido)
                matches = re.finditer('{{(\w*)}}', contenido)
                for i in matches:
                    var = i.group(1)
                    var = var.replace('#', '.')
                    variable = 'this.' + var
                    if variable:
                        contenido = contenido.replace(i.group(0), str(eval(variable)))
                this.cuerpo = contenido


class ReporteAbstract(models.AbstractModel):
    _name = 'report.constancias_multiples.constancia'

    @api.model
    def _get_report_values(self, docids, data=None):
        report_name = 'intn_constancias_multiples.constancia'
        report = self.env['ir.actions.report']._get_report_from_name(report_name)
        return {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': self.env[report.model].browse(docids),
        }


class ConstanciaLineas(models.Model):
    _inherit = 'constancia.lineas'

    constancia_multiple_id = fields.Many2one(
        'constancias.multiples', string="Constancia", required=False, ondelete="cascade")