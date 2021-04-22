from odoo import api, exceptions, fields, models
from datetime import date

class IntnBascula (models.Model):
    _inherit = 'intn.bascula'

    ultimo_informe_id = fields.Many2one('informes.bascula', string='Informe')

    fecha_verificacion = fields.Date(
        'Fecha de Verificación', related="ultimo_informe_id.fecha")

    fecha_vencimiento = fields.Date('Fecha de Vencimiento', related="ultimo_informe_id.fecha_vencimiento")

    resumen_incidencia = fields.Html('Resumen de incidencias', track_visibility="onchange",
                                     related="ultimo_informe_id.resumen_incidencia")

    desperfecto_detalle = fields.Html('Resumen de desperfectos', track_visibility="onchange",
                                      related="ultimo_informe_id.desperfecto_detalle")
    evaluacion = fields.Selection(string="Evaluación visual del instrumento", track_visibility='onchange',
                                  required=False,
                                  selection=[('bueno', 'Bueno'), ('aceptable', 'Aceptable'), ('malo', 'Malo')],
                                  related="ultimo_informe_id.evaluacion_visual")

    informes_ids = fields.Many2many('informes.bascula', string='Informes')

    informes_count = fields.Integer('Informes Count', compute='_compute_informes_count')

    @api.onchange('ultimo_informe_id')
    @api.depends('ultimo_informe_id')
    def computeState(self):
        for this in self:
            if this.ultimo_informe_id:
                today = date.today()
                if today >= this.ultimo_informe_id.fecha_vencimiento:
                    this.write({'state': 'vencido', 'color': 'yellow'})
                else:
                    if this.ultimo_informe_id.evaluacion_final_estado == 'APROBADO':
                        this.write({'state': 'aprobado', 'color': 'green'})
                    if this.ultimo_informe_id.evaluacion_final_estado == 'REPROBADO':
                        this.write({'state': 'reprobado', 'color': 'red'})
                    if this.ultimo_informe_id.bascula_desperfecto:
                        this.write({'state': 'desperfecto', 'color': 'orange'})


    def _compute_informes_count(self):
        for record in self:
            record.computeState()
            record.informes_count = len(record.informes_ids)

    @api.multi
    def action_see_informes(self):
        action = self.env.ref('intn_informe_bascula.informes_bascula_list_view').read()[0]

        informes = self.mapped('informes_ids')
        if len(informes) > 1:
            action['domain'] = [('id', 'in', informes.ids)]
        elif informes:
            form_view = [(self.env.ref('intn_informe_bascula.informes_bascula_form_view').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = informes.id
        return action




