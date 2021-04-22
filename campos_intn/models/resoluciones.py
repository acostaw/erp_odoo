from odoo import models, fields, api,exceptions
from odoo.exceptions import ValidationError


class Resoluciones(models.Model):
    _name = "campos_intn.resoluciones"
    _description = "Formulario para gestion de resoluciones"

    name = fields.Char(string="Número de Resolucion", required=True)
    porcentaje_descuento = fields.Integer(string="Porcentaje (%) de Descuento", required=True)
    nro_expediente = fields.Many2one('sale.order',
                                     ondelete='cascade', string="Expediente Asociado", required=True,
                                     domain=[('state', '=', 'sale')])
    state = fields.Selection(selection=[('draft', 'Borrador'), ('done', 'Confirmado'), ('canceled', 'Cancelado')],
                             string="Estado", default="draft")
    resolucion_pdf = fields.Binary(string="Resolución en PDF")
    pdf_name = fields.Char(string="Resolución en PDF")
    aplica_costos_adicionales = fields.Boolean(string="Aplica a costos adicionales", default=False)

    _sql_constraints = [('nro_expediente_unique', 'UNIQUE(nro_expediente)',
                         "El número de expediente ya está asignado a otra resolución")]



    @api.constrains('porcentaje_descuento')
    def valida_porcentaje(self):
        if self.porcentaje_descuento<1 or self.porcentaje_descuento>100:
            raise exceptions.ValidationError('Porcentaje de descuento incorrecto')
        
    def confirmarResolucion(self):
        for this in self:
            if this.search([('state', '=', 'done'), ('nro_expediente', '=', this.nro_expediente.id)]):
                raise ValidationError('Ya existe una resolución confirmada para este expediente.')
            elif this.nro_expediente.invoice_count:
                raise ValidationError('El expediente ya cuenta con facturas, no se puede aplicar un descuento.')
            else:
                if this.porcentaje_descuento == 100:
                    this.nro_expediente.write({'pago_exonerado':True})
                this.update({'state': 'done'})
                # producto_de_descuento = int(
                #     self.env['ir.config_parameter'].get_param('producto_descuento_parameter')) or False
                producto_de_descuento = self.env['product.template'].browse(int(
                    self.env['ir.config_parameter'].sudo().get_param(
                        'producto_descuento_parameter')) or False).product_variant_id

                # Producto de Costo Adicional
                producto_de_viatico = self.env['product.template'].browse(int(
                    self.env['ir.config_parameter'].sudo().get_param(
                        'producto_viatico_parameter')) or False).product_variant_id

                if not producto_de_descuento:
                    raise ValidationError('Debe asignar un producto como argumento de descuento')
                this.nro_expediente.action_cancel()
                this.nro_expediente.action_draft()
                total = 0
                for line in this.nro_expediente.order_line:
                    if this.aplica_costos_adicionales:
                        if not line.product_id.id == producto_de_descuento.id:
                            total += line.price_unit * line.product_uom_qty
                    else:
                        if not line.product_id.id == producto_de_descuento.id and not line.product_id.id == producto_de_viatico.id:
                            total += line.price_unit * line.product_uom_qty

                descuento = total / 100 * this.porcentaje_descuento * -1

                line_descuento = {
                    'name': producto_de_descuento.name,
                    'product_id': producto_de_descuento.id,
                    'product_uom_qty': 1,
                    'price_unit': descuento,
                    'customer_lead': 0,
                    'order_id': this.nro_expediente.id
                }
                this.env['sale.order.line'].create(line_descuento)
                # this.nro_expediente.update({'order_line': (0, 0, line_descuento)})
                this.nro_expediente.action_confirm()
                self._cr.commit()

    @api.multi
    def unlink(self):
        for this in self:
            if this.state == 'done':
                raise ValidationError('No puede eliminar una resolución confirmada.')
            else:
                super(Resoluciones, self).unlink()
