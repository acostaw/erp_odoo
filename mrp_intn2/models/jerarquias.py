from odoo import fields, api, models, exceptions


class Organismos(models.Model):
    _inherit = 'intn.organismos'
    user_ids = fields.Many2many('res.users',
                                ondelete='cascade', string="Usuarios")

    @api.model_create_multi
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        for val in vals:
            name = val.get('name')
            user_ids = val.get('user_ids')
            if name:
                values_mrp = {
                    'name': name,
                    'user_ids': user_ids
                    # Al nombre del workcenter, le damos el valor del nombre que está viniendo para crear el organismo
                }

                id_workcenter = self.env['mrp.workcenter'].create(
                    values_mrp)  # Se crea el workcenter y se guarda el ID para asignarlo al organismo
                # print(id_workcenter[0])
                val['mrp_workcenter_id'] = id_workcenter.id  # Se actualizan los vals con el id del workcenter
            return super(Organismos, self).create(val)

    # @api.multi
    # def write(self, vals):
    #     for val in vals:
    #         name = val.get('name')
    #         user_ids = val.get('user_ids')
    #         if name:
    #             values_mrp = {
    #                 'name': name,
    #                 'user_ids': user_ids
    #                 # Al nombre del workcenter, le damos el valor del nombre que está viniendo para crear el organismo
    #             }
    #
    #             id_workcenter = self.env['mrp.workcenter'].write(
    #                 values_mrp)
    #         return super(Organismos, self).write(val)

    @api.multi
    def write(self, vals):
        r = super(Organismos, self).write(vals)
        for this in self:
            this.mrp_workcenter_id.update({'name': this.name, 'user_ids': this.user_ids})
        return r

class Unidades(models.Model):
    _inherit = 'intn.unidades'
    user_ids = fields.Many2many('res.users',
                                ondelete='cascade', string="Usuarios")

    @api.model_create_multi
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        for val in vals:
            name = val.get('name')
            user_ids = val.get('user_ids')
            if name:
                values_mrp = {
                    'name': name,
                    'user_ids': user_ids
                    # Al nombre del workcenter, le damos el valor del nombre que está viniendo para crear el organismo
                }

                id_workcenter = self.env['mrp.workcenter'].create(
                    values_mrp)  # Se crea el workcenter y se guarda el ID para asignarlo al organismo
                # print(id_workcenter[0])
                val['mrp_workcenter_id'] = id_workcenter.id  # Se actualizan los vals con el id del workcenter
            return super(Unidades, self).create(val)

    @api.multi
    def write(self, vals):
        r = super(Unidades, self).write(vals)
        for this in self:
            this.mrp_workcenter_id.update({'name': this.name, 'user_ids': this.user_ids})
        return r

class Departamentos(models.Model):
    _inherit = 'intn.departamentos'

    user_ids = fields.Many2many('res.users',
                                ondelete='cascade', string="Usuarios")

    @api.model_create_multi
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        for val in vals:
            name = val.get('name')
            user_ids = val.get('user_ids')
            if name:
                values_mrp = {
                    'name': name,
                    'user_ids': user_ids
                    # Al nombre del workcenter, le damos el valor del nombre que está viniendo para crear el organismo
                }

                id_workcenter = self.env['mrp.workcenter'].create(
                    values_mrp)  # Se crea el workcenter y se guarda el ID para asignarlo al organismo
                # print(id_workcenter[0])
                val['mrp_workcenter_id'] = id_workcenter.id  # Se actualizan los vals con el id del workcenter
            return super(Departamentos, self).create(val)

    @api.multi
    def write(self, vals):
        r = super(Departamentos, self).write(vals)
        for this in self:
            this.mrp_workcenter_id.update({'name': this.name, 'user_ids': this.user_ids})
        return r


class Coordinaciones(models.Model):
    _inherit = 'intn.coordinaciones'

    user_ids = fields.Many2many('res.users',
                                ondelete='cascade', string="Usuarios")

    @api.model_create_multi
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        for val in vals:
            name = val.get('name')
            user_ids = val.get('user_ids')
            if name:
                values_mrp = {
                    'name': name,
                    'user_ids': user_ids
                    # Al nombre del workcenter, le damos el valor del nombre que está viniendo para crear el organismo
                }

                id_workcenter = self.env['mrp.workcenter'].create(
                    values_mrp)  # Se crea el workcenter y se guarda el ID para asignarlo al organismo
                # print(id_workcenter[0])
                val['mrp_workcenter_id'] = id_workcenter.id  # Se actualizan los vals con el id del workcenter
            return super(Coordinaciones, self).create(val)

    @api.multi
    def write(self, vals):
        r = super(Coordinaciones, self).write(vals)
        for this in self:
            this.mrp_workcenter_id.update({'name': this.name, 'user_ids': this.user_ids})
        return r


class Laboratorios(models.Model):
    _inherit = 'intn.laboratorios'

    user_ids = fields.Many2many('res.users',
                                ondelete='cascade', string="Usuarios")
    @api.model_create_multi
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        for val in vals:
            name = val.get('name')
            user_ids = val.get('user_ids')
            if name:
                values_mrp = {
                    'name': name,
                    'user_ids': user_ids
                    # Al nombre del workcenter, le damos el valor del nombre que está viniendo para crear el organismo
                }

                id_workcenter = self.env['mrp.workcenter'].create(
                    values_mrp)  # Se crea el workcenter y se guarda el ID para asignarlo al organismo
                # print(id_workcenter[0])
                val['mrp_workcenter_id'] = id_workcenter.id  # Se actualizan los vals con el id del workcenter
            return super(Laboratorios, self).create(val)

    @api.multi
    def write(self, vals):
        r = super(Laboratorios, self).write(vals)
        for this in self:
            this.mrp_workcenter_id.update({'name': this.name,'user_ids': this.user_ids})
        return r
