from odoo import models, api, fields, exceptions
import qrcode
import base64,hashlib
from io import BytesIO


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    qr_code = fields.Binary(string="QR Code", compute="generate_qr_code")

    @api.multi
    def action_invoice_open(self):
        super(AccountInvoice, self).action_invoice_open()
        return super(AccountInvoice, self).action_invoice_sent()


    def genera_token(self,id_factura):
        palabra=id_factura+"amakakeruriunohirameki"
        return hashlib.sha256(bytes(palabra,'utf-8')).hexdigest()

    def generate_qr_code(self):
        for i in self:
            base_url = self.env['ir.config_parameter'].sudo(
            ).get_param('web.base.url')
            route = "/invoice_check?invoice_id="+str(i.id)+"&token="+i.genera_token(str(i.id))
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data("%s%s" % (base_url, route))
            qr.make(fit=True)
            img = qr.make_image()
            temp = BytesIO()
            img.save(temp, format="PNG")
            qr_image = base64.b64encode(temp.getvalue())
            i.qr_code = qr_image


    def format_linea_autoimpresor(self, linea=False):
        limite = 50
        if not linea:
            return False
        else:
            linea_limitada = []
            linea_actual = ''
            c = 0
            for i in linea:
                c += 1
                linea_actual += i
                if c == limite:
                    linea_limitada.append(linea_actual)
                    linea_actual = ''
                    c = 0
            if linea_actual: linea_limitada.append(linea_actual)
            return linea_limitada
