from odoo import models, fields, api


class saleOrder(models.Model):
    _inherit = "sale.order"

    producto = fields.Char(string="Producto ")

    alcance = fields.Text(string="Alcance")

    notas_especiales = fields.Text(string="Notas Especiales")

    solicitante_id = fields.Many2one('res.partner', string="Solicitante")



class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    etapas = fields.Selection([
        ('etapa_inicial', "Etapa Inicial"),
        ('etapa_uno', "Etapa I"),
        ('etapa_dos', "Etapa II"),
        ('etapa_tres', 'Etapa III'),
        ('etapa_vigilancia', 'Etapa de Vigilancia')], required=False, default=False, string="Etapas", compute="_computeEtapa")



    @api.depends('product_id')
    def _computeEtapa(self):
        for this in self:
            this.etapas = this.product_id.etapas



