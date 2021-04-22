from odoo import fields, api, models, exceptions
from odoo.tools import float_round

class mrpProduction(models.Model):
    _inherit = 'mrp.production'


    def _workorders_create(self, bom, bom_data):
        workorders = super(mrpProduction, self)._workorders_create(bom,bom_data)
        dict_departamento_ids=[]

        for i in workorders:
            vals={}
            if i.production_id:
                vals['sale_order_id']=i.production_id.origin
            if i.product_id and i.product_id.departamento_id and i.product_id.departamento_id.sequence_id and not dict_departamento_ids:
                secuencia=i.product_id.departamento_id.sequence_id.sudo().next_by_id()
                vals['numero_informe']=secuencia
                dict_departamento_ids.append({str(i.product_id.departamento_id.id):secuencia})
            elif i.product_id and i.product_id.departamento_id and i.product_id.departamento_id.sequence_id and dict_departamento_ids:
                for m in dict_departamento_ids:
                    if m.get(str(i.product_id.departamento_id.id)):
                        vals['numero_informe']=m.get(str(i.product_id.departamento_id.id))
                    else:
                        secuencia=i.product_id.departamento_id.sequence_id.sudo().next_by_id()
                        vals['numero_informe']=secuencia
                        dict_departamento_ids.append({str(i.product_id.departamento_id.id):secuencia})
            if i.product_id and i.product_id.unidad_id and i.product_id.unidad_id.sequence_id and not vals.get('numero_informe'):
                vals['numero_informe']=i.product_id.unidad_id.sequence_id.sudo().next_by_id()
            i.with_context(viene_de_crear=True).write(vals)
        return workorders
