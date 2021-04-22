# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
import operator


class InformesBasculaReportWizard(models.TransientModel):
    _name = 'informes_bascula.report.wizard'

    date_start = fields.Date(string="Fecha Inicio", required=True, default=fields.Date.today)
    date_end = fields.Date(string="Fecha Final", required=True, default=fields.Date.today)
    user_ids = fields.Many2many('res.users', string="Funcionarios Comisionados",required=True)

    @api.multi
    def get_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_start': self.date_start,
                'date_end': self.date_end,
                'user_ids': self.user_ids.ids,
            },
        }

        return self.env.ref('intn_informe_bascula.recap_report').report_action(self, data=data)


class ReportInformesBascula(models.AbstractModel):

    _name = 'report.intn_informe_bascula.recap_report_view'

    @api.model
    def _get_report_values(self, docids, data=None):
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        user_ids = data['form']['user_ids']
        date_start_obj = datetime.strptime(date_start, DATE_FORMAT)
        date_end_obj = datetime.strptime(date_end, DATE_FORMAT)


        start_report = date_start_obj.strftime('%d/%m/%Y')
        end_report = date_end_obj.strftime('%d/%m/%Y')

        docs = []
        comercios = []
        departamentos = []
        ciudades = []
        meses = []
        users = []

        if user_ids:
            informes = self.env['informes.bascula'].search(
                [('state', 'in', ['done','cancel']),
                 ('fecha', '>=', date_start_obj.strftime(DATETIME_FORMAT)),
                 ('fecha', '<=', date_end_obj.strftime(DATETIME_FORMAT))]).filtered(
                    lambda x: x.tecnico_id.id in user_ids)

        if informes:
            users = informes.mapped('tecnico_id')
            comercios = len(set(informes.mapped('partner_id')))
            departamentos = set(informes.mapped('state_id'))
            ciudades = set(informes.mapped('city'))
            meses = set(informes.mapped('mes'))
            docs = sorted(informes, key = lambda x: x.fecha)


        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_start': start_report,
            'date_end': end_report,
            'docs': docs,
            'users':users,
            'departamentos':departamentos,
            'ciudades': ciudades,
            'comercion':comercios,
            'meses':meses
        }
