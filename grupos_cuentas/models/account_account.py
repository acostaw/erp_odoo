from odoo import fields, api, models, exceptions


class AccountAccount(models.Model):
    _inherit = 'account.account'
    _order = 'display_code'

    _sql_constraints = [
        ('code_company_uniq', 'check(1=1)', 'El codigo de la cuenta debe ser unico por compañia!')
    ]

    display_code = fields.Char('Código', compute="mostrar_codigo", store=True)

    @api.multi
    @api.depends('code', 'group_id')
    def mostrar_codigo(self):
        for i in self:
            group = i.group_id
            i.display_code = i.code
            while group:
                i.display_code = group.code_prefix + "." + i.display_code
                group = group.parent_id
            # i.display_code = codigos_grupos + "." + i.code

    def name_get(self):
        result = []
        for i in self:
            name = i.name
            if i.display_code:
                name = i.display_code + ' ' + name
            #        name = i.code + " " + name
            result.append((i.id, name))
        return result

    @api.constrains('code', 'group_id')
    def _validar_duplicados(self):
        codigo_nuevo = self.code
        if self.group_id:
            id_group = self.group_id.id
        else:
            id_group = False

        duplicados = self.env['account.account'].search(
            [('company_id', '=', self.env.user.company_id.id), ('id', '!=', self.id), ('group_id', '=', id_group),
             ('code', '=', codigo_nuevo)])

        if duplicados:
            raise exceptions.ValidationError('Ya existe una cuenta con éste código/prefijo en éste grupo.')

    @api.onchange('code')
    def onchange_code(self):
        return None

    @api.model
    def create(self, vals):
        return super(AccountAccount, self).create(vals)

    @api.multi
    def write(self, vals):
        return super(AccountAccount, self).write(vals)


class AccountGroup(models.Model):
    _inherit = 'account.group'
    _order = 'display_code'

    code_prefix = fields.Char(required=True)

    # display_name = fields.Char(string='Nombre', _compute="name_get", store=True)
    # child_ids = fields.One2many('account.group', 'parent_id')
    display_code = fields.Char('Código', compute="mostrar_codigo", store=True)

    @api.multi
    @api.depends('code_prefix', 'parent_id')
    def mostrar_codigo(self):
        for i in self:
            parent = i.parent_id
            i.display_code = i.code_prefix
            while parent:
                i.display_code = parent.code_prefix + "." + i.display_code
                parent = parent.parent_id

    def name_get(self):
        result = []
        for group in self:
            name = group.name
            if group.display_code:
                name = group.display_code + ' ' + name
            result.append((group.id, name))
        return result

    @api.constrains('code_prefix', 'parent_id')
    def _validar_duplicados(self):
        codigo_nuevo = self.code_prefix
        if self.parent_id:
            id_parent = self.parent_id.id
        else:
            id_parent = False

        duplicados = self.env['account.group'].search([('id', '!=', self.id), ('parent_id', '=', id_parent),
                                                       ('code_prefix', '=', codigo_nuevo)])
        #        else:
        #           duplicados = self.env['account.group'].search([('id', '!=', self.id), ('code_prefix', '=', codigo_nuevo)])
        if duplicados:
            raise exceptions.ValidationError('Ya existe éste código/prefijo en éste grupo.')

    @api.model
    def create(self, vals):
        return super(AccountGroup, self).create(vals)

    @api.multi
    def write(self, vals):
        return super(AccountGroup, self).write(vals)
