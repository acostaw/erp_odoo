from odoo import models, fields, api
from odoo.exceptions import ValidationError


class res_expediente(models.Model):
    _inherit = "sale.order"

    resolucion_id = fields.Many2one('campos_intn.resoluciones', string="Nro Resolucion", compute='_get_resolucion_id')
    contrato_id = fields.Many2one('intn.contrato', string='Contrato', default=False, copy=False)
    necesita_contrato = fields.Boolean('Necesita contrato', compute='_necesita_contrato')
    pago_exonerado = fields.Boolean('Se exonera el pago', compute='_pago_exonerado',store=True, default=False, copy=False, track_visibility='onchange')


    #   DESCRIPCION TRABAJO:
    descripcion_trabajos = fields.Text(string='Descripción de los Trabajos')
    materiales_entregados = fields.Text(string='Materiales Entregados')
    fecha_entrega = fields.Date(string='Fecha de Entrega')

    #   Translado
    distancia_ida = fields.Integer('Distancia', help='Distancia en kilometros (sólo ida)')
    costo_peaje = fields.Monetary('Costo peaje', help='Costo total a pagar en los puestos de peaje')
    precio_combustible = fields.Monetary('Precio combustible', help='Precio (por litro) del combustible utilizado')
    vehiculo_id = fields.Many2one('intn.vehiculo', string='Vehículo')
    vehiculo_con_carga = fields.Boolean(string='Con peso',
                                        help='El vehiculo lleva carga, por lo tanto, el consumo de combustible del mismo sube')
    costo_translado = fields.Monetary('Costo de traslado', compute='_compute_costo_translado')
    ciudad_muestreo_id = fields.Many2one('intn.costo.traslado.muestreo', string='Ciudad/Dpto')
    costo_translado_muestreo = fields.Monetary('Costo de Traslado ',compute="_onChangeCiudadMuestreo")
    #   Viático
    departamento_id = fields.Many2one('res.country.state', string='Departamento del país',
                                      domain=[('departamento_paraguay', '=', True)],
                                      default=lambda x: x.partner_id.state_id)
    cantidad_tecnicos = fields.Integer('Cantidad de Técnicos', default=0)
    dias_pernoctados = fields.Integer('Días pernoctados')
    dias_no_pernoctados = fields.Integer('Días no pernoctados')
    costo_viatico = fields.Monetary('Costo de Viaticos', compute='_compute_costo_viatico')

    solicitante = fields.Char(string="Solicitante")

    #Gastos Administrativos Normas
    gastos_administrativos = fields.Monetary(string='Total Gastos Administrativos', compute='_compute_gastos_administrativos')
    porcentaje_gastos_administrativos = fields.Selection(string="Gastos Administrativos", selection=[('diez', '10%'), (
        'treinta', '30%')], default='')


    #Costo Adicional Horas Extras
    sueldo = fields.Monetary('Sueldo')
    horas_extras = fields.Integer('Horas Extras')
    costo_horas_extras = fields.Monetary('Costo total Horas Extra', compute='_compute_costo_horas_extra')

    @api.onchange('ciudad_muestreo_id')
    def _onChangeCiudadMuestreo(self):
        for this in self:
            this.costo_translado_muestreo = this.ciudad_muestreo_id.monto


    @api.depends('distancia_ida', 'precio_combustible', 'vehiculo_id', 'vehiculo_con_carga', 'costo_peaje')
    def _compute_costo_translado(self):
        for this in self:
            a = 0
            if not (this.distancia_ida > 0 and this.precio_combustible > 0 and this.vehiculo_id):
                this.costo_translado = 0
            else:
                litro_por_kilometro = (
                                          this.vehiculo_id.consumo_con_carga if this.vehiculo_con_carga else this.vehiculo_id.consumo_sin_carga) / 100
                this.costo_translado = this.costo_peaje + 2 * (
                        this.precio_combustible * this.distancia_ida * litro_por_kilometro)

    @api.depends('porcentaje_gastos_administrativos', 'amount_total')
    def _compute_gastos_administrativos(self):
        for this in self:
            if this.porcentaje_gastos_administrativos:
                total_gastos_envio = this.amount_total
                producto_gastos_envio = self.env['product.template'].browse(int(
                    self.env['ir.config_parameter'].sudo().get_param(
                        'producto_gastos_envio_parameter')) or False).product_variant_id
                for line in this.order_line:
                    if line.product_id.id == producto_gastos_envio.id:
                        total_gastos_envio = this.amount_total - line.price_total
                if this.porcentaje_gastos_administrativos == 'diez':
                    this.gastos_administrativos = (total_gastos_envio * 10) / 100
                elif this.porcentaje_gastos_administrativos == 'treinta':
                    this.gastos_administrativos = (total_gastos_envio * 30) / 100

    @api.depends('sueldo','horas_extras')
    def _compute_costo_horas_extra(self):
        for this in self:
            if not this.sueldo and this.horas_extras:
                this.costo_horas_extras = 0
            else:
                this.costo_horas_extras = int(this.sueldo/30/8/1.7) * this.horas_extras

    @api.depends('departamento_id', 'dias_pernoctados', 'dias_no_pernoctados', 'cantidad_tecnicos')
    def _compute_costo_viatico(self):
        for this in self:
            if not this.departamento_id and this.cantidad_tecnicos:
                this.costo_viatico = 0
            elif this.departamento_id.fecha_vigencia and this.departamento_id.fecha_vigencia < this.date_order:
                raise ValidationError('Monto de víatico está Vencido')
            else:
                this.costo_viatico = ((this.departamento_id.viatico_monto * this.dias_pernoctados) + (
                        this.departamento_id.viatico_monto * this.dias_no_pernoctados) / 2) * this.cantidad_tecnicos

    @api.multi
    def write(self, values):

        for this in self:
            r = super(res_expediente, self).write(values)
            if (this.costo_viatico > 0 or this.costo_translado > 0 or this.costo_translado_muestreo > 0 or this.costo_horas_extras) and not self.env['ir.config_parameter'].sudo().get_param(
                    'producto_viatico_parameter'):
                raise ValidationError('Necesita establecer un producto que se utilizará para los costos adicionales')
            elif this.gastos_administrativos and not self.env['ir.config_parameter'].sudo().get_param(
                    'producto_gastos_envio_parameter'):
                raise ValidationError(
                    'Necesita establecer un producto que se utilizará para los gastos administrativos por envio')
            else:
                if this.costo_viatico or this.costo_translado or this.costo_translado_muestreo or this.costo_horas_extras or this.gastos_administrativos:
                    this.set_linea_viatico()
            return r

    @api.multi
    def action_confirm(self):
        for this in self:
            if this.necesita_contrato and not this.contrato_id:
                raise ValidationError(
                    'Necesita crear y confirmar un contrato para éste expediente antes de confirmarlo')
            elif (this.costo_viatico > 0 or this.costo_translado > 0) and not self.env['ir.config_parameter'].sudo().get_param(
                    'producto_viatico_parameter'):
                raise ValidationError('Necesita establecer un producto que se utilizará para los costos adicionales')
            elif this.gastos_administrativos and not self.env['ir.config_parameter'].sudo().get_param(
                    'producto_gastos_envio_parameter'):
                raise ValidationError('Necesita establecer un producto que se utilizará para los gastos administrativos por envio')
            else:
                if this.costo_viatico or this.costo_translado or this.costo_translado_muestreo or this.costo_horas_extras or this.gastos_administrativos: this.set_linea_viatico()
                if this.departamento_id and this.departamento_id.fecha_vigencia and this.departamento_id.fecha_vigencia < this.date_order:
                    raise ValidationError('Monto de víatico está Vencido')
                return super(res_expediente, self).action_confirm()

    def set_linea_viatico(self):
        if self.costo_translado or self.costo_viatico or self.costo_translado_muestreo or  self.costo_horas_extras:
            linea_viatico_existente = False
            producto_de_viatico = self.env['product.template'].browse(int(
                self.env['ir.config_parameter'].sudo().get_param(
                    'producto_viatico_parameter')) or False).product_variant_id
            for line in self.order_line:
                if line.product_id.id == producto_de_viatico.id: linea_viatico_existente = line

            if linea_viatico_existente:
                linea_viatico_existente.update({'price_unit': self.costo_translado + self.costo_viatico + self.costo_translado_muestreo +  self.costo_horas_extras})
            else:
                line_viatico = {
                    'name': producto_de_viatico.name,
                    'product_id': producto_de_viatico.id,
                    'product_uom_qty': 1,
                    'price_unit': self.costo_translado + self.costo_viatico + self.costo_translado_muestreo  + self.costo_horas_extras,
                    'customer_lead': 0,
                    'order_id': self.id
                }
                self.env['sale.order.line'].create(line_viatico)

        if self.gastos_administrativos:
            linea_gastos_envio_existente = False
            producto_gastos_envio = self.env['product.template'].browse(int(
                self.env['ir.config_parameter'].sudo().get_param(
                    'producto_gastos_envio_parameter')) or False).product_variant_id
            for line in self.order_line:
                if line.product_id.id == producto_gastos_envio.id: linea_gastos_envio_existente = line

            if linea_gastos_envio_existente:
                linea_gastos_envio_existente.update({'price_unit': self.gastos_administrativos})
            else:
                line_gastos_envio = {
                    'name': producto_gastos_envio.name,
                    'product_id': producto_gastos_envio.id,
                    'product_uom_qty': 1,
                    'price_unit': self.gastos_administrativos,
                    'customer_lead': 0,
                    'order_id': self.id
                }
                self.env['sale.order.line'].create(line_gastos_envio)

    def _get_resolucion_id(self):
        for this in self:
            this.resolucion_id = this.resolucion_id.search([('state', '=', 'done'), ('nro_expediente', '=', this.id)])

    # def _get_contrato_id(self):
    #     for this in self:
    #         contrato = this.contrato_id.search([('state', '=', 'done'), ('sale_order_id', '=', this.id)])
    #         if contrato:
    #             this.update({'payment_term_id': False})
    #         self._cr.commit()
    #         this.contrato_id = contrato.id

    def _pago_exonerado(self):
        for this in self:
            pago_exonerado = True if this.resolucion_id and this.resolucion_id.porcentaje_descuento >= 100 else False
            if pago_exonerado:
                # Producto de Costo Adicional
                producto_de_viatico = self.env['product.template'].browse(int(
                    self.env['ir.config_parameter'].sudo().get_param(
                        'producto_viatico_parameter')) or False).product_variant_id
                for line in this.order_line:
                    if line.product_id.id == producto_de_viatico.id:
                        pago_exonerado = False
            this.pago_exonerado = pago_exonerado



    @api.depends('order_line')
    def _necesita_contrato(self):
        for this in self:
            if not this.contrato_id or this.contrato_id.state != 'done':
                for line in this.order_line:
                    if line.product_id.organismo_id and line.product_id.organismo_id.necesita_contrato:
                        this.necesita_contrato = True
                    else:
                        if line.product_id.unidad_id and line.product_id.unidad_id.necesita_contrato:
                            this.necesita_contrato = True
                        else:
                            if line.product_id.departamento_id and line.product_id.departamento_id.necesita_contrato:
                                this.necesita_contrato = True
                            else:
                                if line.product_id.coordinacion_id and line.product_id.coordinacion_id.necesita_contrato:
                                    this.necesita_contrato = True
                                else:
                                    if line.product_id.laboratorio_id and line.product_id.laboratorio_id.necesita_contrato:
                                        this.necesita_contrato = True
                                    break

    @api.multi
    def _prepare_invoice(self):
        for i in self:
            inv=super(res_expediente,i)._prepare_invoice()
            recevaible=inv.get('account_id')
            if not recevaible:
                partner=self.env['res.partner'].browse(inv.get('partner_id'))
                inv['account_id']=partner.property_account_receivable_id.id or partner.commercial_partner_id.property_account_receivable_id.id
            return inv
