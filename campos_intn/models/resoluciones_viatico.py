from odoo import models, fields, api,exceptions
from odoo.exceptions import ValidationError


class ResolucionesViatico(models.Model):
    _name = "campos_intn.resoluciones_viatico"

    state_id = fields.Many2one('res.country.state', string='Departamento del país',
                                      domain=[('departamento_paraguay', '=', True)])

    name = fields.Char(string="Nro de Resolución", required=True)
    monto = fields.Integer(string="Monto", required=True)
    fecha_vigencia = fields.Datetime(string="Fecha Finalización vigencia", required=True)
    state = fields.Selection(selection=[('draft', 'Borrador'), ('done', 'Confirmado'), ('canceled', 'Cancelado')],
                             string="Estado", default="draft")

    name = fields.Char(string='Nombre')



    def confirmarResolucion(self):
        for this in self:
        #     if this.search([('state', '=', 'done'), ('state_id', '=', this.state_id.id)]):
        #         raise ValidationError('Ya existe una resolución confirmada para este departamento.')
        #     else:
                this.update({'state': 'done'})