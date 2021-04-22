from odoo import fields, models, api


class ResConfigSettingsCompras(models.TransientModel):
    _inherit = 'res.config.settings'

    producto_descuento = fields.Many2one('product.template', string="Producto de Descuento",
                                         default_model='res.config.settings')
    producto_viatico = fields.Many2one('product.template', string="Producto de Viático",
                                       default_model='res.config.settings')
    producto_gastos_envio = fields.Many2one('product.template', string="Producto Gastos Administrativos por Envío",
                                       default_model='res.config.settings')

    @api.multi
    def set_values(self):
        self.env['ir.config_parameter'].sudo().set_param('producto_descuento_parameter',
                                                  self.producto_descuento.id)
        self.env['ir.config_parameter'].sudo().set_param('producto_viatico_parameter',
                                                  self.producto_viatico.id)
        self.env['ir.config_parameter'].sudo().set_param('producto_gastos_envio_parameter',
                                                  self.producto_gastos_envio.id)

        super(ResConfigSettingsCompras, self).set_values()

    @api.model
    def get_values(self):
        res = super(ResConfigSettingsCompras, self).get_values()
        res.update(
            producto_descuento=int(
                self.env['ir.config_parameter'].sudo().get_param('producto_descuento_parameter')) or False,
            producto_viatico=int(self.env['ir.config_parameter'].sudo().get_param('producto_viatico_parameter')) or False,
            producto_gastos_envio=int(self.env['ir.config_parameter'].sudo().get_param('producto_gastos_envio_parameter')) or False,
        )
        return res
