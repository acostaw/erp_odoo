from odoo import fields, api, models, exceptions
from odoo.exceptions import UserError

class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    derivado = fields.Many2one('mrp.workcenter')
    devolucion_exigida = fields.Boolean(string='Devolucion exigida', default=False)
    user_derivado = fields.Boolean(string='Usuario Derivado',default=False,compute="_usuario_derivado")
    numero_informe = fields.Char(string="Numero de Informe")
    sale_order_id = fields.Char(string='Nro de Expediente')
    descripcion_trabajos =fields.Text(compute="descripcionesAdicionales",string="Descripción trabajos")
    materiales_entregados = fields.Text(string="Materiales Entregados")
    nombre_retiro= fields.Char(string='Nombre')
    ci_retiro = fields.Char(string='Nro de C.I')
    fecha_retiro = fields.Datetime(string="Fecha y Hora")
    observacion = fields.Text(string="Observación")

    sale_order = fields.Many2one('sale.order', string="Nro Expediente", compute="m2o_sale_order",store=True)

    partner_id = fields.Many2one('res.partner', string="Cliente", store=True, related="sale_order.partner_id")
    # partner = fields.Many2one('res.partner', string="Cliente",compute='WorkorderPartner')


    solicitud_interna_id = fields.Many2one('mrp.workorder.solicitud_interna', string="Nro Solicitud Interna")

    # @api.multi
    def m2o_sale_order(self):
        for rec in self:
            if rec.sale_order_id:
                sale_order = self.env['sale.order'].search(
                    [('name','=',rec.sale_order_id)])
                rec.sale_order = sale_order.id



    def descripcionesAdicionales(self):
        for this in self:
            if this.sale_order_id:
                expediente = self.env['sale.order'].search([['name', '=', this.production_id.origin]])
                if expediente.descripcion_trabajos:
                    this.descripcion_trabajos = expediente.descripcion_trabajos
                if expediente.materiales_entregados:
                    this.materiales_entregados = expediente.materiales_entregados



    # @api.onchange('numero_informe')
    def numeroInforme(self,sale_order_id,numero_informe,departamento_id):
            workorders = self.env['mrp.workorder'].search([['production_id', 'ilike', sale_order_id]])
            for workorder in workorders:
                # if not workorder.sale_order_id  and workorder.state != 'done':
                #     workorder.write({'sale_order_id': sale_order_id})
                if workorder.numero_informe != numero_informe and workorder.state != 'done':
                    if workorder.product_id.departamento_id.id == departamento_id:
                        workorder.write({'numero_informe': numero_informe})

    @api.multi
    def numeroExpediente(self):
        for this in self:
            if this.production_id:
                expediente = self.env['sale.order'].search([['name', '=', this.production_id.origin]])
                if this.state != 'done':
                    this.write({'sale_order_id': expediente.name})

    @api.multi
    def write(self, values):
        r = super(MrpWorkorder, self).write(values)
        for this in self:
           if this._context.get('viene_de_crear') != True:
               if 'numero_informe' in values:
                 departamento_id = this.product_id.departamento_id
                 departamento_id = departamento_id.id
                 self.env['mrp.workorder'].numeroInforme(this.production_id.origin,this.numero_informe,departamento_id)
        return r

    def button_start(self):
        for i in self:
            if self.env.uid not in self.workcenter_id.user_ids.ids:
                raise exceptions.ValidationError(
                    'No tiene permisos para ejecutar Ordenes de Trabajo en éste Centro de Producción')
            op = i.production_id
            secuencia = i.operation_id.sequence
            ots_anteriores = op.workorder_ids.filtered(
                lambda x: x.operation_id.sequence < secuencia and x.id != i.id)
            for j in ots_anteriores:
                if j.state != 'done':
                    raise exceptions.ValidationError(
                        'No se puede empezar una Orden de trabajo si existen anteriores no finalizadas')
            if i.state != 'done':
                i.date_planned_start = fields.Datetime.now()
            super(MrpWorkorder, i).button_start()

    def button_derivar(self):
        view = self.env.ref(
            'mrp_intn2.mrp_workcenter_derivar_wizard_view')
        return {
            'name': 'Derivar a',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mrp.workorder.derivar',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': {'default_workorder_id': self.id},
        }

    def button_solicitud_interna(self):
        view = self.env.ref(
            'mrp_intn2.mrp_workcenter_derivar_wizard_view')
        return {
            'name': 'Derivar a',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mrp.workorder.derivar',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': {'default_workorder_id': self.id,'default_solicitud_interna': True},
        }

    @api.multi
    def record_production(self):
        if self.devolucion_exigida:
            self.button_pending()
            self.write(
                {'state': 'ready', 'workcenter_id': self.derivado.id, 'devolucion_exigida': False, 'derivado': None})
        elif not self.devolucion_exigida and self.derivado:
            self.write(
                {'state': 'ready', 'workcenter_id': self.derivado.id, 'devolucion_exigida': False, 'derivado': None})
            return super(MrpWorkorder, self).record_production()
        else:
            return super(MrpWorkorder, self).record_production()

    def batch_start_orders(self):
        for this in self:
            if this.state == 'ready':
                this.button_start()

    def batch_conclude_orders(self):
        for this in self:
            if this.state == 'progress':
                this.record_production()

    @api.model
    def button_derivar_multi(self, workorders):

        view = self.env.ref(
            'mrp_intn2.mrp_workcenter_derivar_wizard_view')
        return {
            'name': 'Derivar a',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mrp.workorder.derivar',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': {'default_workorder_ids': [(6, 0, workorders.ids)]},
        }

    def _usuario_derivado(self):
        for this in self:
            usuario_actual = self._uid
            if this.derivado and this.solicitud_interna_id:
                for users in this.workcenter_id.user_ids:
                    user_id = users.id
                    if user_id == usuario_actual:
                        this.user_derivado = True
                    else:
                        this.user_derivado = False
            else:
                this.user_derivado = False
