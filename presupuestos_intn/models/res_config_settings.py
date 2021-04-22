from odoo import fields, models, api


class ResConfigSettingsExpedientes(models.TransientModel):
    _inherit = 'res.config.settings'

    version_metrologia = fields.Char(string="Version Metrologia",
                                         default_model='res.config.settings')

    @api.multi
    def set_values(self):
        self.env['ir.config_parameter'].sudo().set_param('version_metrologia_parameter',
                                                         self.version_metrologia)
        super(ResConfigSettingsExpedientes, self).set_values()

    @api.model
    def get_values(self):
        res = super(ResConfigSettingsExpedientes, self).get_values()
        res.update(
            version_metrologia=self.env['ir.config_parameter'].sudo().get_param('version_metrologia_parameter'),

        )
        return res