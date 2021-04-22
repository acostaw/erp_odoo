# -*- coding: utf-8 -*-

from odoo import models, api, fields, exceptions
import qrcode
import base64
import hashlib
from io import BytesIO
from odoo.exceptions import ValidationError
import datetime


class IntnConstancias(models.Model):
    _name = 'intn.constancias'
    _inherit = ['mail.thread', 'mail.activity.mixin'] #agregar al nuevo modulo.

    name = fields.Char('Número', default="Borrador",
                       track_visibility='onchange', copy=False) #track_visi
    order_id = fields.Many2one(
        'sale.order', string="Expediente", required=True)
    solicitante_id = fields.Many2one('res.partner', string="Solicitante")
    fecha_expediente = fields.Datetime('Fecha de Expediente')
    state = fields.Selection(string='Estado', selection=[(
        'draft', 'Borrador'), ('done', 'Confirmado'), ('cancel', 'Cancelado')], default='draft',
        track_visibility='onchange')
    fecha_informe = fields.Datetime(
        'Fecha de Informe', default=lambda self: fields.Datetime.now())
    departamento_id = fields.Many2one('intn.departamentos')
    descripcion1 = fields.Html('Descripcion 1', default='Conforme al Expediente <b>$expediente</b>, presentada por la empresa'
                                                        '<b>&nbsp; $solicitante</b> en la cual solicita un Informe Técnico referente a la '
                                                        'importación de <b>$producto</b> amparado en la Factura Comercial Nº&nbsp;<b>$factura</b> de '
                                                        'la empresa <b>&nbsp; $proveedor</b> .')
    descripcion2 = fields.Html('Descripcion 2', default="Se informa que el producto mencionado en la factura &nbsp;"
                                                        "<b>&nbsp;NO requiere la certificación del ONC – INTN, conforme a las "
                                                        "disposiciones establecidas en la Resolución MIC Nº 803/2018.</b>")
    factura_comercial = fields.Char('Factura Comercial')
    proveedor = fields.Char('Proveedor')
    qr_code = fields.Binary(string="QR Code", compute="generate_qr_code")
    line_ids = fields.One2many(
        'constancia.lineas', 'constancia_id', string='Lineas', copy=True)
    cantidadImpresiones = fields.Integer(default=0, copy=False)
    user_id = fields.Many2one('res.users', 'Usuario',
                              default=lambda self: self.env.user)
    nombre_imprimir = fields.Char(string="Nombre del cliente a imprimir")

    @api.onchange('solicitante_id')
    def obtener_nombre(self):
        for i in self:
            if i.solicitante_id:
                i.update({'nombre_imprimir': i.solicitante_id.name})

    @api.model_create_multi
    @api.returns('self', lambda value: value.id)
    def create(self, vals_list):
        res = super(IntnConstancias, self).create(vals_list)
        descripcion1 = res.descripcion1
        if res.order_id:
            descripcion1 = descripcion1.replace(
                "$expediente",res.order_id.name)
        if res.solicitante_id:
            descripcion1 = descripcion1.replace(
                "$solicitante", res.nombre_imprimir)
        if res.line_ids:
            descripcion1 = descripcion1.replace(
                "$producto",res.line_ids[0].product_id.determinacion)
        if res.factura_comercial:
            descripcion1 = descripcion1.replace(
                "$factura",res.factura_comercial)
        if res.proveedor:
            descripcion1 = descripcion1.replace("$proveedor",res.proveedor)
        res.write({'descripcion1': descripcion1})
        return res

    @api.onchange('order_id')
    def onchangeorder(self):
        for this in self:
            this.update({'line_ids': [(5, 0, 0)]})
            if this.order_id:
                this.solicitante_id = this.order_id.partner_id.id
                this.fecha_expediente = this.order_id.confirmation_date
                lines = []
                product_count = 0
                for line in this.order_id.order_line:
                    for product in line.product_id:
                        product_count += 1
                        if product_count > 1:
                            raise ValidationError(
                                'El expediente seleccionado cuenta con más de un producto')
                        else:
                            this.departamento_id = product.departamento_id
                            d = {
                                'product_id': product.id,
                            }
                            lines.append((0, 0, d))
                this.update({'line_ids': lines})

    def genera_token(self, id_factura):
        palabra = id_factura+"amakakeruriunohirameki"
        return hashlib.sha256(bytes(palabra, 'utf-8')).hexdigest()

    def generate_qr_code(self):
        for i in self:
            base_url = self.env['ir.config_parameter'].sudo(
            ).get_param('web.base.url')
            route = "/constancia_check?constancia_id=" + \
                str(i.id)+"&token="+i.genera_token(str(i.id))
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data("%s%s" % (base_url, route))
            qr.make(fit=True)
            img = qr.make_image()
            temp = BytesIO()
            img.save(temp, format="PNG")
            qr_image = base64.b64encode(temp.getvalue())
            i.qr_code = qr_image

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

    @api.multi
    def button_print(self):
        return self.env.ref('intn_constancias.reporte_constancia').report_action(self)

    @api.multi
    def button_send(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference(
                'intn.constancias', 'intn_constancias.email_template')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference(
                'mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {
            'default_model': 'intn.constancias',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'force_email': True
        }
        r = {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }
        if r:
            return r

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

    def cantImpresiones(self):
        for this in self:
            if this.state == 'draft' or this.state == 'cancel':
                return True
            else:
                this.cantidadImpresiones = this.cantidadImpresiones + 1
                if this.cantidadImpresiones > 20:
                    return True
                else:
                    return False


class ConstanciaLineas(models.Model):
    _name = 'constancia.lineas'

    constancia_id = fields.Many2one(
        'intn.constancias', string="Constancia", required=False,ondelete="cascade")
    product_id = fields.Many2one(
        'product.product', string='Producto/Servicio', required=True)
