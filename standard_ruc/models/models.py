# -*- coding: utf-8 -*-
from odoo import models, fields, exceptions, api
import re


class agregar(models.Model):
    _inherit = 'res.partner'

    is_company = fields.Boolean(default=True)

    @api.depends('vat')
    def val_ruc(self,vals):
        ruc=None
        if vals.get('vat'):
            ruc = vals['vat']
        elif self.vat:
            ruc = self.vat
        if self.is_company:
            if ruc:
                def digito_verificador(ruc):
                    ruc_asd = str(ruc).split("-")
                    ruc_ci = ruc_asd[0]
                    ruc_str = str(ruc_ci)[::-1]
                    v_total = 0
                    basemax = 11
                    k = 2
                    for i in range(0, len(ruc_str)):
                        if k > basemax:
                            k = 2
                        v_total += int(ruc_str[i]) * k
                        k += 1
                        resto = v_total % basemax
                    if resto > 1:
                        return basemax - resto
                    else:
                        return 0

                pattern = "^[0-9]+-[0-9]$"
                if re.match(pattern, ruc):
                    lista1 = self.env['res.partner'].search(
                        [('vat', '=', ruc), ('company_id', '=', self.env.user.company_id.id),('id','!=',self.id)])
                    if len(lista1) > 1:
                        raise exceptions.ValidationError("RUC ya existente!")
                    else:
                        ruc_das = str(ruc).split("-")
                        ruc_dig = ruc_das[1]
                        if (str(digito_verificador(ruc)) != ruc_dig):
                            raise exceptions.ValidationError(
                                "El digito verificador deberia de ser " + str(digito_verificador(ruc)))
                else:
                    raise exceptions.ValidationError("Error de formato de RUC! (Ejemplo: 12345678-9)")
            else:
                #raise exceptions.ValidationError('Debe agregar un RUC')
                return


    @api.model
    def create(self,vals):
        self.val_ruc(vals)
        return super(agregar,self).create(vals)

    def write(self,vals):
        self.val_ruc(vals)
        return super(agregar,self).write(vals)



class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def create(self, vals):
        vals.update({'is_company': False})
        user = super(ResUsers, self).create(vals)
        user.partner_id.active = user.active
        if user.partner_id.company_id:
            user.partner_id.write({'company_id': user.company_id.id})

        return user
