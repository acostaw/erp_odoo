from odoo import fields, api, models, exceptions

class WizardDerivar(models.TransientModel):
    _name = 'mrp.workorder.derivar'

    workcenter_id = fields.Many2one(
        'mrp.workcenter', string="Centro de produccion", required=True)
    workorder_id = fields.Many2one('mrp.workorder', string="Orden de trabajo")
    workorder_ids = fields.Many2many('mrp.workorder', string="Ordenes de trabajo")
    exigir_devolucion=fields.Boolean('Exigir devolucion',default=True)
    solicitud_interna=fields.Boolean('Solicitud Interna',default=False)

    def button_derivar(self):
        for i in self:
            if i.workorder_id:
                anterior = i.workorder_id.workcenter_id
                if i.solicitud_interna:
                    data = {
                        'workcenter_id': self.workcenter_id.id,
                        'workorder_id': i.workorder_id.id,
                        'workcenter_derivado_id': anterior.id
                    }
                    id_solicitud_interna = self.env['mrp.workorder.solicitud_interna'].create(
                        data)
                    i.workorder_id.write(
                        {'workcenter_id': self.workcenter_id.id, 'derivado': anterior.id, 'solicitud_interna_id':id_solicitud_interna.id,
                         'devolucion_exigida': self.exigir_devolucion})
                else:
                    i.workorder_id.write(
                        {'workcenter_id': self.workcenter_id.id, 'derivado': anterior.id,'devolucion_exigida':self.exigir_devolucion})
            if i.workorder_ids:
                for workorder in i.workorder_ids:
                    anterior = workorder.workcenter_id
                    workorder.write(
                        {'workcenter_id': self.workcenter_id.id, 'derivado': anterior.id,
                         'devolucion_exigida': self.exigir_devolucion})
