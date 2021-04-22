# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import datetime,math,locale
from odoo.exceptions import ValidationError

class TerminosCondiciones(models.Model):
    _inherit = "sale.order"
    terms = fields.Char(compute='_terms')
    termsAdministrativos = fields.Char(compute='_terms')
    es_metrologia = fields.Boolean (compute='_esMetrologia')
    fecha = fields.Date(
        string='Fecha', default=fields.Date.today(), required=True, track_visibility='onchange')
    fecha_letras = fields.Char(compute='_fechaLetras')
    departamento_responsable = fields.Char(default='',compute='_termsAdministrativos')

    lpi = fields.Char(string="LPI")

    user_id = fields.Many2one('res.users', string='Comercial',copy=False, index=True, track_visibility='onchange', track_sequence=2, default=lambda self: self.env.user)

    def _fechaLetras(self):
        for this in self:
            this.fecha_letras = this.date_order.strftime("%d de %B de %Y")

    def _terms(self):
        for this in self:
            organismos = []
            unidades = []
            departamentos = []
            coordinaciones = []
            laboratorios =[]
            terminosOrg = ""
            terminosUni = ""
            terminosDep = ""
            terminosCoo = ""
            terminosLab = ""
            for l in this.order_line:
                if l.product_id.organismo_id and l.product_id.organismo_id not in organismos:
                    organismos.append(l.product_id.organismo_id)
                    if l.product_id.organismo_id.terms:
                        terminosOrg = terminosOrg + "\n" + l.product_id.organismo_id.terms

                if l.product_id.unidad_id and l.product_id.unidad_id not in unidades:
                    unidades.append(l.product_id.unidad_id)
                    if l.product_id.unidad_id.terms:
                        terminosUni = terminosUni +"\n" + l.product_id.unidad_id.terms

                if l.product_id.departamento_id and l.product_id.departamento_id not in departamentos:
                    departamentos.append(l.product_id.departamento_id)
                    if l.product_id.departamento_id.terms:
                        terminosDep = terminosDep +"\n" + l.product_id.departamento_id.terms

                if l.product_id.coordinacion_id and l.product_id.coordinacion_id not in coordinaciones:
                    coordinaciones.append(l.product_id.coordinacion_id)
                    if l.product_id.coordinacion_id.terms:
                        terminosCoo = terminosCoo +"\n" + l.product_id.coordinacion_id.terms

                if l.product_id.laboratorio_id and l.product_id.laboratorio_id not in laboratorios:
                    laboratorios.append(l.product_id.laboratorio_id)
                    if l.product_id.laboratorio_id.terms:
                        terminosLab = terminosLab + "\n" + l.product_id.laboratorio_id.terms

            terminos = terminosOrg + terminosUni + terminosDep + terminosCoo + terminosLab
            this.termsAdministrativos = terminos

    def _termsAdministrativos(self):
        for this in self:
            departamentos = []
            terminos = ""
            for l in this.order_line:
                if l.product_id.departamento_id and l.product_id.departamento_id.name not in departamentos:
                    departamentos.append(l.product_id.departamento_id.name)
                    if l.product_id.departamento_id.terms:
                        terminos = l.product_id.departamento_id.terms + "\n"
            # this.termsAdministrativos = terminos
            this.departamento_responsable = ''
            for n in departamentos:
                this.departamento_responsable = this.departamento_responsable + ' - ' + n


    def _firmasResponsables(self):
        for this in self:
            departamentos = []
            responsables = []
            for l in this.order_line:
                if l.product_id.departamento_id and l.product_id.departamento_id not in departamentos:
                    departamentos.append(l.product_id.departamento_id)
                    if l.product_id.departamento_id.partner_id:
                        responsable = l.product_id.departamento_id.partner_id
                        responsables.append({'name': responsable.name, 'email': responsable.email, 'phone': responsable.phone, 'depto': l.product_id.departamento_id.name})
        return responsables

    def _esMetrologia(self):
        for this in self:
            for l in this.order_line:
                if l.product_id.organismo_id and 'ONM' in l.product_id.organismo_id.name:
                    this.es_metrologia = 'True'

    @api.multi
    def action_cancel(self):
        for this in self:
            facturas = self.env['account.invoice'].search(
                [('type', '=', 'out_invoice'), ('state', 'in', ['open', 'paid', 'in_payment']),
                 ('origin', '=', this.name)])
            # print(facturas)
            if facturas:
                raise exceptions.ValidationError(
                    'No puede eliminar un expediente que tenga facturas validadas asociadas.')
            return super(TerminosCondiciones, self).action_cancel()

class ReporteAbstract(models.AbstractModel):
    _name = 'report.presupuestos_intn.expediente'

    @api.model
    def _get_report_values(self, docids, data=None):
        report_name = 'presupuestos_intn.expediente'
        report = self.env['ir.actions.report']._get_report_from_name(report_name)
        return {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': self.env[report.model].browse(docids),
            'firmas': self.env['sale.order'].browse(docids)._firmasResponsables(),
            'version_metrologia': self.env['ir.config_parameter'].sudo().get_param(
                    'version_metrologia_parameter')
        }