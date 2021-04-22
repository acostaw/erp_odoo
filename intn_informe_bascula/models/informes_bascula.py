# -*- coding: utf-8 -*-
import datetime
import itertools
from datetime import date

import dateutil
from dateutil.relativedelta import relativedelta
from odoo import models, api, fields, exceptions
from lxml import etree
from odoo.exceptions import ValidationError
from openerp.osv.orm import setup_modifiers
import re
import uuid
import qrcode
import base64
import hashlib
from io import BytesIO


class InformesBascula(models.Model):
    _name = 'informes.bascula'
    _description = 'Informes Bascula'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'
    #     pantilla_constancia_id = fields.Many2one('plantila.constancias')

    name = fields.Char('Número', default="Borrador",
                       track_visibility='onchange', copy=False, required=True)
    fecha = fields.Date(
        'Fecha', default=lambda self: fields.Date.today())

    fecha_vencimiento = fields.Date('Fecha de Vencimiento')

    vigencia_meses = fields.Integer(default=12, required=True,string="Vigencia (en meses)")

    order_id = fields.Many2one(
        'sale.order', string="Expediente", required=True)

    fecha_estimada = fields.Date(
        string='Fecha estimada de servicio', track_visibility='onchange', readonly=False, related="order_id.fecha_estimada",
        copy=False)

    tecnico_id = fields.Many2one('res.users', string='Técnico asignado', required=True, track_visibility='onchange', readonly=False, default=lambda self: self.env.user, copy=False)

    invoice_id = fields.Many2one('account.invoice', string="Factura", requiered=True)

    partner_id = fields.Many2one('res.partner', string="Cliente", related="order_id.partner_id", store=True)

    street = fields.Char('Dirección', related="partner_id.street")

    city = fields.Char('Ciudad', related="partner_id.city")

    state_id = fields.Many2one('res.country.state', related="partner_id.state_id", string="Departamento")

    ruc = fields.Char('RUC', related="partner_id.vat")

    calcomania_nro = fields.Char(string='Calcomania nro', required=False, copy=False)

    ##################################################

    recibido_por = fields.Char(string='Informe recibido por ', required=True, copy=True, track_visibility='onchange')
    ci_contacto = fields.Char(string="CI del Contacto", required=True, copy=True, track_visibility='onchange')

    ##################################################

    bascula_id = fields.Many2one('intn.bascula', string='Báscula', track_visibility="onchange", required=True, readonly=False, related="order_id.bascula_id")

    marca = fields.Selection(string='Marca', selection=[(
        'toledo', 'Toledo'), ('mettler_toledo', 'Mettler Toledo'), ('saturno','Saturno'), ('filizola', 'Filizola'), ('dina','Dina'), ('sin_datos', 'Sin datos'), ('otros','Otros')],
                             track_visibility='onchange', related="bascula_id.marca")
    carga_maxima = fields.Float(stirng='Carga Máxima', related="bascula_id.carga_max", readonly=False)
    rubro = fields.Char(stirng='Rubro', related="bascula_id.rubro",selection=[('comercio', 'Comercio')])
    modelo = fields.Char(stirng='Modelo', related="bascula_id.modelo")
    nro_serie = fields.Char(stirng='Número de serie', related="bascula_id.no_serie")
    tipo = fields.Selection(string='Tipo', selection=[(
        'electronico', 'Electrónico'), ('mecanico', 'Mecánico'), ('hibrido','Híbrido')],
                            track_visibility='onchange', related="bascula_id.tipo")
    carga_minima = fields.Float(stirng='Carga mínima', related="bascula_id.carga_min")
    division_e_d = fields.Float(stirng='División', related="bascula_id.division", readonly=False,selection=[('10', '10'), ('20', '20')])
    clase = fields.Selection(string='Clase', selection=[(
        'iii', 'III'), ('iv', 'IV')], related="bascula_id.clase")
    patron_trabajo = fields.Char(string='Patrón de trabajo', copy=False)

    bascula_desperfecto = fields.Boolean('Báscula con Desperfectos', default=False, track_visibility="onchange")
    desperfecto_detalle = fields.Html('Observación', track_visibility="onchange")

    evaluacion_visual = fields.Selection(string='Evaluación Visual del instrumento', selection=[(
        'bueno', 'Bueno'), ('aceptable', 'Aceptable'), ('malo','Malo')], required=True)
    evaluacion_general = fields.Text(stirng='Evaluación general del instrumento', copy=False)

    exentricidad_carga_aplicada = fields.Float('Carga aplicada', default=0.0, copy=False)
    exentricidad_max_error = fields.Float('Máx. Error', default=0.0, copy=False)
    exentricidad_aprobado = fields.Boolean('Aprobado', copy=False)
    fidelidad_carga_aplicada = fields.Float('Carga aplicada', default=0.0, copy=False)
    fidelidad_max_error = fields.Float('Máx. Error', default=0.0, copy=False)
    fidelidad_aprobado = fields.Boolean('Aprobado', copy=False)
    carga_aplicada_cero = fields.Float('Carga aplicada cercana al cero', default=0.0, copy=False)
    exactitud_cero_aprobado = fields.Boolean('Aprobado', copy=False)
    sensibilidad_carga = fields.Float('Es sensible a una carga de', default=0.0, copy=False)
    mobilidad_aprobado = fields.Boolean('Aprobado', copy=False)
    max_error_encontrado = fields.Float('Máximo error encontrado', default=0.0, copy=False)
    desem_carga_aprobado = fields.Boolean('Aprobado', copy=False)

    line_ids = fields.One2many(
        'constancia.lineas', 'informes_bascula_id', string='Lineas de Expediente', copy=False)

    line_ensayos_ids = fields.One2many(
        'informes.bascula.lines', 'informe_bascula_id', string='Lineas', copy=False)

    state = fields.Selection(string='Estado', selection=[(
        'draft', 'Borrador'), ('done', 'Confirmado'), ('cancel', 'Cancelado')], default='draft',
                             track_visibility='onchange', copy=False)

    user_id = fields.Many2one('res.users', 'Usuario',
                              default=lambda self: self.env.user, copy=False)

    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env['res.company'])

    calificacion = fields.Char(string='Calificacion', track_visibility='onchange', copy=False)
    feedback = fields.Text(string='Comentario', track_visibility='onchange', copy=False)

    evaluacion_final_estado = fields.Selection(string='Evaluación final', selection=[(
        'APROBADO', 'APROBADO'), ('REPROBADO', 'REPROBADO')], default="REPROBADO", compute='evaluacionFinal', copy=False)
    evaluacion_final_comentario = fields.Text('Evaluación final del instrumento', copy=False)


    #~~~~~~Registro de incidencia~~~~~~~~~
    resumen_incidencia = fields.Html('Resumen de incidencias', track_visibility="onchange")
    acta_pdf = fields.Binary(string='Acta en PDF', track_visibility="onchange")
    pdf_name = fields.Char(string='pdf_name')


    state_bascula = fields.Selection(string="Estado de la báscula", track_visibility='onchange', selection=[('aprobado', 'APROBADO'), ('reprobado', 'REPROBADO'),('desperfecto','Imposibilidad de Verificación por Desperfecto'),('vencido','Vencido')], related="bascula_id.state"  )


    kg_pesas = fields.Selection(string="Kg pesas", track_visibility='onchange', selection=[('1000', '1000'), ('500', '500')], required=True)
    pesas_num = fields.Integer('Pesas')

    mes = fields.Selection(compute="onchangeFecha",selection=[('01', 'Enero'), ('02', 'Febrero'),('03','Marzo'),('04','Abril'),('05','Mayo'),('06','Junio'),('07','Julio'),('08','Agosto'),('09','Setiembre'),('10','Octubre'),('11','Noviembre'),('12','Diciembre')])

    @api.onchange('kg_pesas')
    @api.depends('kg_pesas')
    def onchangePesas(self):
        for this in self:
            peso = this.kg_pesas
            this.pesas_num = int(peso)


    @api.depends('exentricidad_aprobado', 'fidelidad_aprobado', 'exactitud_cero_aprobado', 'mobilidad_aprobado',
                 'desem_carga_aprobado','line_ensayos_ids')
    def evaluacionFinal(self):
        for this in self:
            if not this.exentricidad_aprobado or not this.fidelidad_aprobado or not this.exactitud_cero_aprobado or not this.mobilidad_aprobado or not this.desem_carga_aprobado:
                this.evaluacion_final_estado = 'REPROBADO'
            else:
                this.evaluacion_final_estado = 'APROBADO'
            mayor = 0
            for line in this.line_ensayos_ids:
                if abs(line.error_kg) > mayor:
                    mayor = abs(line.error_kg)
                if abs(line.error_kg) != line.mep_kg:
                    this.evaluacion_final_estado = 'REPROBADO'
            this.max_error_encontrado = mayor


    def _default_access_token(self):
        return uuid.uuid4().hex

    access_url = fields.Char('URL del portal de cliente', compute="_compute_access_url")
    access_token = fields.Char('Token de seguridad', default=_default_access_token)

    qr_code = fields.Binary(string="QR Code", compute="generate_qr_code")

    @api.multi
    def _get_report_base_filename(self):
        self.ensure_one()
        return '%s %s' % ('Constancia', self.name)

    def _compute_access_url(self):
        # super(SolicitudesServicio, self)._compute_access_url()
        for informe in self:
            informe.access_url = '/my/informes/bascula/%s' % (informe.id)

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
    def onchangeOrderBascula(self):
        self.bascula_id = False
        if self.order_id:
            basculas_partner = self.order_id.partner_id.bascula_ids
            basculas_child = self.order_id.partner_id.child_ids
            id = []
            for child in basculas_child:
                for bascula in child.bascula_ids:
                    id.append(child.id)
            return {'domain': {'bascula_id': ['|' ,('id', '=', basculas_partner.ids),('id','=',id)]}}
        else:
            return {'domain': {'bascula_id': []}}

    @api.onchange('order_id')
    @api.depends('order_id')
    def onchangeorder(self):
        for this in self:
            this.update({'line_ids': [(5, 0, 0)]})
            if this.order_id:
                factura = self.env['account.invoice'].search(
                    [('origin', '=', this.order_id.name), ('state', 'not in', ['draft,cancel'])])[0]
                if factura:
                    this.update({'invoice_id': factura.id})
                lines = []
                product_count = 0
                for line in this.order_id.order_line:
                    for product in line.product_id:
                        product_count += 1
                        if product_count > 1:
                            raise ValidationError(
                                'El expediente seleccionado cuenta con más de un producto')
                        else:
                            d = {
                                'product_id': product.id,
                            }
                            lines.append((0, 0, d))
                this.update({'line_ids': lines})

    def button_confirmar(self):
        for i in self:
            i.asigna_nombre()
            date_1 = datetime.datetime.strptime(str(i.fecha), "%Y-%m-%d")
            i.fecha_vencimiento = i.fecha + relativedelta(months=i.vigencia_meses)
            # i.fecha_vencimiento = datetime.datetime.strptime(str(i.fecha_vencimiento), "%Y-%m-%d")
            i.write({'state': 'done'})
            i.bascula_id.write({'informes_ids':[(4,i.id,0)], 'ultimo_informe_id':i.id})
            i.bascula_id.computeState()
            template_id = self.env.ref('intn_informe_bascula.email_template_confirmacion').id
            self.env['mail.template'].browse(template_id).send_mail(self.id, force_send=True)

    def button_cancelar(self):
        for i in self:
            if i.invoice_id:
                i.invoice_id.action_invoice_cancel()
            if i.order_id:
                i.order_id.action_cancel()
            i.write({'state': 'cancel'})

    def button_draft(self):
        for i in self:
            i.write({'state': 'draft'})

    def genera_secuencia(self):
        seq = self.sudo().env['ir.sequence'].next_by_code('seq_informe_bascula')
        if seq:
            return seq
        else:
            raise ValidationError('Debe asignar el codigo de secuencia del informe')


    @api.depends('tecnico_id')
    @api.onchange('tecnico_id')
    def asigna_calcomania(self):
        for i in self:
            seq = self.env['calcomanias.tecnicos'].search([('tecnico_id','=',self.tecnico_id.id)])
            if not seq:
                raise ValidationError(
                    'Debe asignar al técnido un rango de numeración de calcomanias antes de crear el informe')
            new_name = str(seq.sgte_numero).zfill(7)
            i.update({'calcomania_nro': new_name})

    def asigna_nombre(self):
        for i in self:
            if self.name and self.name == 'Borrador':
                seq = self.env['numeracion.informe.tecnicos'].search([('tecnico_id','=',self.tecnico_id.id)])
                if not seq:
                    raise ValidationError(
                        'Debe asignar al técnido un rango de numeración de informe antes de confirmar el informe')
                new_name = seq.numeracion_id.prefijo + str(seq.sgte_numero).zfill(7)
                seq.write({'sgte_numero':seq.sgte_numero +1})
                i.write({'name': new_name})
                seq_calcomania = self.env['calcomanias.tecnicos'].search([('tecnico_id', '=', self.tecnico_id.id)])
                if not seq_calcomania:
                    raise ValidationError(
                        'Debe asignar al técnido un rango de numeración de calcomanias antes de confirmar el informe')
                new_name_calc = str(seq.sgte_numero).zfill(7)
                i.write({'calcomania_nro':new_name_calc})
                seq_calcomania.write({'sgte_numero': seq_calcomania.sgte_numero + 1})
            else:
                return

    @api.model_create_multi
    @api.returns('self', lambda value: value.id)
    def create(self, vals_list):
        res = super(InformesBascula, self).create(vals_list)
        for i in res:
            reg = {
                'res_id': i.id,
                'res_model': 'informes.bascula',
                'partner_id': i.partner_id.id
            }
            follower_id = self.env['mail.followers'].create(reg)
        return res


    def genera_token(self, id_informe):
        palabra = id_informe+"amakakeruriunohirameki"
        return hashlib.sha256(bytes(palabra, 'utf-8')).hexdigest()

    def generate_qr_code(self):
        for i in self:
            base_url = self.env['ir.config_parameter'].sudo(
            ).get_param('web.base.url')
            route = "/my/informes/bascula/check?id=" + \
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


    def send_email_vencimiento(self):
        template_id = self.env.ref('intn_informe_bascula.email_template_vencimiento').id
        self.env['mail.template'].browse(template_id).send_mail(self.id,force_send=True)

    @api.onchange('line_ensayos_ids')
    @api.depends('line_ensayos_ids')
    def actualiza_nro_linea(self):
        for i in self:
            cont = 1
            for line in i.line_ensayos_ids:
                line.update({'nro_linea': cont})
                cont += 1

    def enviar_mail_vencimiento_ipna(self):
        present = datetime.datetime.now()
        presente = dateutil.parser.parse(str(present)).date()
        inf_vencidos = self.env['informes.bascula'].search(
            [('fecha_vencimiento', '=', date.today())])
        for v in inf_vencidos:
            v.bascula_id.write({'state':'vencido'})
        informes_a_vencer = self.env['informes.bascula'].search(
            [('fecha_vencimiento', '=', presente + datetime.timedelta(days=30))])
        for inf in informes_a_vencer:
            inf.send_email_vencimiento()

    @api.onchange('fecha')
    @api.depends('fecha')
    def onchangeFecha(self):
        for this in self:
            if this.fecha:
                mes = this.fecha.strftime('%m')
                this.mes = mes

class ReporteAbstract(models.AbstractModel):
    _name = 'report.informes_bascula.informe'

    @api.model
    def _get_report_values(self, docids, data=None):
        report_name = 'intn_informes_bascula.informe'
        report = self.env['ir.actions.report']._get_report_from_name(report_name)
        return {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': self.env[report.model].browse(docids),
        }


class ConstanciaLineas(models.Model):
    _inherit = 'constancia.lineas'

    informes_bascula_id = fields.Many2one(
        'informes.bascula', string="Informe Bascula", required=False, ondelete="cascade")


class InformesBasculaLines(models.Model):
    _name = 'informes.bascula.lines'

    informe_bascula_id = fields.Many2one(
        'informes.bascula', string="Informe Bascula", required=False, ondelete="cascade")

    division = fields.Float('Division', related="informe_bascula_id.division_e_d",selection=[('10', '10'), ('20', '20')])
    kg_pesas = fields.Integer('Pesas', related="informe_bascula_id.pesas_num", readonly=False)

    carga_kg = fields.Float('Carga (kg)', default=0.0, compute='computeCarga', store=True)
    indicacion_kg = fields.Float('Indicación (kg)', default=0.0)
    error_kg = fields.Float('Error (kg)', default=0.0, compute='computeError', store=True)
    mep_kg = fields.Float('MEP (+-kg)', default=0.0, readonly=True, compute='computeMEP',store=True)

    state = fields.Selection(string='Estado', selection=[(
        'draft', 'Borrador'), ('done', 'Confirmado'), ('cancel', 'Cancelado')], default='draft',
                             track_visibility='onchange', related="informe_bascula_id.state")

    nro_linea = fields.Integer(string="Nro. linea",store=True)

    @api.onchange('carga_kg','indicacion_kg')
    @api.depends('carga_kg','indicacion_kg')
    def computeError(self):
        for this in self:
            this.update({'error_kg':this.carga_kg-this.indicacion_kg})
            #this.error_kg = this.carga_kg-this.indicacion_kg

    @api.onchange('carga_kg', 'division')
    @api.depends('carga_kg', 'division')
    def computeMEP(self):
        for this in self:
            if this.division == '10':
                if 500 <= this.carga_kg <= 5000:
                    #this.mep_kg = 10
                    this.update({'mep_kg': 10})
                elif 5000 < this.carga_kg <= 20000:
                    this.update({'mep_kg': 20})
                elif 20000 < this.carga_kg <= this.informe_bascula_id.carga_maxima:
                    this.update({'mep_kg': 30})
            if this.division == '20':
                if 500 <= this.carga_kg <= 10000:
                    this.update({'mep_kg': 20})
                elif 10000 < this.carga_kg <= this.informe_bascula_id.carga_maxima:
                    this.update({'mep_kg': 40})

    @api.onchange('nro_linea','kg_pesas')
    @api.depends('kg_pesas','nro_linea')
    def computeCarga(self):
        for this in self:
            this.update ({'carga_kg': this.kg_pesas * this.nro_linea})
            #this.carga_kg = this.kg_pesas * this.nro_linea