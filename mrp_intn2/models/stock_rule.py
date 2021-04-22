from odoo import fields, api, models, exceptions

import logging
_logger = logging.getLogger(__name__)


class StockRule(models.Model):
    _inherit = 'stock.rule'

    @api.multi
    def _run_manufacture(self, product_id, product_qty, product_uom, location_id, name, origin, values):
        Production = self.env['mrp.production']
        ProductionSudo = Production.sudo().with_context(
            force_company=values['company_id'].id)
        bom = self._get_matching_bom(product_id, values)
        if not bom:
            msg = 'No existe una lista de materiales para el producto %s. Por favor defina una.' % (
                product_id.display_name,)
            raise exceptions.UserError(msg)

        # create the MO as SUPERUSER because the current user may not have the rights to do it (mto product launched by a sale for example)
        if product_id and product_id.unidad_id and product_id.unidad_id.genera_ordenes_cantidad:
            for i in range(0, int(product_qty)):
                production = ProductionSudo.create(self._prepare_mo_vals(
                    product_id, 1, product_uom, location_id, name, origin, values, bom))
                origin_production = values.get(
                    'move_dest_ids') and values['move_dest_ids'][0].raw_material_production_id or False
                orderpoint = values.get('orderpoint_id')
                if orderpoint:
                    production.message_post_with_view('mail.message_origin_link',
                                                      values={
                                                          'self': production, 'origin': orderpoint},
                                                      subtype_id=self.env.ref('mail.mt_note').id)
                if origin_production:
                    production.message_post_with_view('mail.message_origin_link',
                                                      values={
                                                          'self': production, 'origin': origin_production},
                                                      subtype_id=self.env.ref('mail.mt_note').id)

        else:
            production = ProductionSudo.create(self._prepare_mo_vals(
                product_id, product_qty, product_uom, location_id, name, origin, values, bom))
            origin_production = values.get(
                'move_dest_ids') and values['move_dest_ids'][0].raw_material_production_id or False
            orderpoint = values.get('orderpoint_id')
            if orderpoint:
                production.message_post_with_view('mail.message_origin_link',
                                                  values={
                                                      'self': production, 'origin': orderpoint},
                                                  subtype_id=self.env.ref('mail.mt_note').id)
            if origin_production:
                production.message_post_with_view('mail.message_origin_link',
                                                  values={
                                                      'self': production, 'origin': origin_production},
                                                  subtype_id=self.env.ref('mail.mt_note').id)
        return True
