from odoo import fields, api, models, exceptions


class SolicitudInterna(models.Model):
    _name = 'mrp.workorder.solicitud_interna'

    name = fields.Char(string='Numero ')
    workcenter_id = fields.Many2one(
        'mrp.workcenter', string="Centro de produccion", required=True)
    workorder_id = fields.Many2one('mrp.workorder', string="Orden de trabajo")
    workcenter_derivado_id = fields.Many2one(
        'mrp.workcenter', string="Centro de produccion Anterior", required=True)

    def asigna_nombre(self):
        for i in self:
            new_name = self.sudo().env['ir.sequence'].next_by_code('seq_solicitud_interna')
            i.write({'name': new_name})

    @api.model
    def create(self, vals):
        r = super(SolicitudInterna, self).create(vals)
        r.asigna_nombre()
        print(r.name)
        return r
