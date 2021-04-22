from odoo import api, exceptions, fields, models


class IntnBascula(models.Model):
    _name = 'intn.bascula'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Número', default="Báscula", track_visibility='onchange', copy=False)  # track_visi

    marca = fields.Selection(string="Marca", selection=[(
        'otros', 'Otros'), ('sin_datos', 'Sin datos'),
        ('dina', 'Dina'), ('filizola', 'Filizola'),
        ('saturno', 'Saturno'), ('mettler_toledo', 'Mettler Toledo'),
        ('toledo', 'Toledo')], track_visibility='onchange', required=True)

    carga_max = fields.Float(string="Carga máxima", track_visibility='onchange', required=True)

    rubro = fields.Char(string="Rubro", track_visibility='onchange', required=True,selection=[('comercio', 'Comercio')])

    modelo = fields.Char(string="Modelo", track_visibility='onchange', required=True)

    no_serie = fields.Char(string="Número de serie", track_visibility='onchange', required=True)

    tipo = fields.Selection(string="Tipo", track_visibility='onchange', required=True,
                            selection=[('electronico', 'Electronico'), ('mecanico', 'Mecanico'),
                                       ('hibrido', 'Hibrido')])

    carga_min = fields.Float(string="Carga mínima", track_visibility='onchange', required=True)

    division = fields.Float(string="División", track_visibility='onchange', required=True,selection=[('10', '10'), ('20', '20')])

    clase = fields.Selection(string='Clase', selection=[('iii', 'III'), ('iv', 'IV')], track_visibility='onchange',
                             required=True)

    encargado = fields.Char(string="Encargado de la báscula", track_visibility='onchange', required=True)

    state = fields.Selection(string="Estado de la báscula", track_visibility='onchange',
                             selection=[('aprobado', 'Aprobado'), ('reprobado', 'Reprobado'),
                                        ('desperfecto', 'Imposibilidad de Verificación por Desperfecto'),
                                        ('vencido', 'Vencido')])

    color = fields.Char(string="Color")

    partner_id = fields.Many2one('res.partner', string='Cliente', required=False, track_visibility='onchange')

    @api.model_create_multi
    def create(self, vals_list):
        res = super(IntnBascula, self).create(vals_list)
        for i in res:
            i.name = i.no_serie
            if not i in i.partner_id.bascula_ids:
                i.partner_id.write({'bascula_ids':[(4,i.id,0)]})
        return res

    @api.multi
    def write(self, values):
        partner_anterior = self.partner_id
        res = super(IntnBascula, self).write(values)
        if res and values.get('no_serie'):
            self.name = self.no_serie
        if not self in self.partner_id.bascula_ids:
            self.partner_id.write({'bascula_ids': [(4, self.id, 0)]})
        if partner_anterior != self.partner_id:
            self.partner_id.write({'bascula_ids': [(3, self.id, 0)]})
        return res



