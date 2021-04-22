import datetime

from odoo import api, exceptions, fields, models
from odoo.exceptions import ValidationError

class CalcomaniasInforme (models.Model):
    _name = 'calcomanias.informe'
    _rec_name = 'year'
    _description = 'Calcomanias Informes'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.model
    def year_selection(self):
        year = 2021  # replace 2000 with your a start year
        year_list = []
        while year != 2030:  # replace 2030 with your end year
            year_list.append((str(year), str(year)))
            year += 1
        return year_list

    year = fields.Selection(year_selection, string='Año',store=True, required=True, track_visibility='onchange')

    nro_inicial = fields.Integer('Número Inicial', required=True, track_visibility='onchange')

    nro_final = fields.Integer('Número Final', required=True, track_visibility='onchange')

    sgte_numero = fields.Integer('Siguiente Número', required=True, track_visibility='onchange')

    active = fields.Boolean(string="Activo", default=True)

    color = fields.Char('Color', required=True, track_visibility='onchange')

    @api.onchange('nro_inicial')
    @api.depends('nro_inicial')
    def sgteNumero(self):
        for this in self:
            this.sgte_numero = this.nro_inicial




class CalcomaniasTecnicos (models.Model):
    _name = 'calcomanias.tecnicos'
    _description = 'Calcomanias Tecnicos'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'tecnico_id'

    calcomania_id = fields.Many2one('calcomanias.informe', string='Calcomanía',store=True, required=True, domain=[('active', '=', True)])

    tecnico_id = fields.Many2one('res.users', string='Técnico asignado', required=True, track_visibility='onchange')

    nro_inicial = fields.Integer('Número Inicial', required=True, track_visibility='onchange', store=True, readonly=True)

    nro_final = fields.Integer('Número Final', required=True, track_visibility='onchange')

    sgte_numero = fields.Integer('Siguiente Número', required=True, track_visibility='onchange')

    active = fields.Boolean(string="Activo", default=True, related="calcomania_id.active")

    @api.onchange('calcomania_id')
    @api.depends('calcomania_id')
    def nroInicial(self):
        for this in self:
            this.nro_inicial = this.calcomania_id.sgte_numero
            #this.update({'nro_inicial':this.calcomania_id.sgte_numero})

    @api.onchange('nro_final', 'calcomania_id')
    @api.depends('nro_final', 'calcomania_id')
    def checkNumeroFinal(self):
        for this in self:
            if this.calcomania_id and this.nro_final:
                if this.nro_final > this.calcomania_id.nro_final:
                    raise ValidationError(
                        'No puede asignar un número mayor al número final de la numeración activa')

    @api.onchange('nro_inicial')
    @api.depends('nro_inicial')
    def sgteNumero(self):
        for this in self:
            this.sgte_numero = this.nro_inicial

    @api.model_create_multi
    @api.returns('self', lambda value: value.id)
    def create(self, vals_list):
        res = super(CalcomaniasTecnicos, self).create(vals_list)
        for i in res:
            i.calcomania_id.write({'sgte_numero':i.nro_final + 1})
        return res

    @api.multi
    def write(self, vals):
        res = super(CalcomaniasTecnicos, self).write(vals)
        self.calcomania_id.write({'sgte_numero': self.nro_final + 1})
        return  res
