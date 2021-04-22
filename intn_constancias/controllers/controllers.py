# -*- coding: utf-8 -*-
from odoo import http
import hashlib

class IntnConstancias(http.Controller):
    @http.route('/constancia_check', auth='public', website=True)
    def index(self,constancia_id,token):
        if token==self.genera_token(str(constancia_id)):
            constancia=http.request.env['intn.constancias'].sudo().search([('id','=',int(constancia_id)),('state','=','done')])
            return http.request.render('intn_constancias.online_constancia',{'constancia':constancia})
        else:
            return http.request.render('intn_constancias.token_invalido')

    def genera_token(self,id_constancia):
        palabra=id_constancia+"amakakeruriunohirameki"
        return hashlib.sha256(bytes(palabra,'utf-8')).hexdigest()