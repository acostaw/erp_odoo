# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from . import amount_to_text_spanish


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    pedido_materiales_equipos = fields.Boolean(string="Pedido de materiales y/o equipos", related="picking_type_id.pedido_materiales_equipos")
    retiro_materiales_equipos = fields.Boolean(string="Orden de retiro de materiales y/o equipos", related="picking_type_id.retiro_materiales_equipos")

    necesita_aprobacion = fields.Boolean(string="Necesita aprobacion", compute='computeNecesitaAprobacion')

    aprobado = fields.Boolean(string="Aprobado", track_visibility="onchange")

    puede_aprobar = fields.Boolean(string="Puede aprobar", compute="computePuedeAprobar")

    organismo_solicitante_id = fields.Many2one('intn.organismos', string="Organismo Solicitante", required=False,
                                               track_visibility='onchange')
    unidad_solicitante_id = fields.Many2one('intn.unidades', string="Unidad Solicitante", track_visibility='onchange',
                                            required=False)
    dpto_solicitante_id = fields.Many2one('intn.departamentos', string="Departamento Solicitante",
                                          track_visibility='onchange', required=False)

    fecha_letras = fields.Char(compute='_fechaLetras')

    justificacion_pedido = fields.Text(string="Justificación del pedido")

    def _fechaLetras(self):
        for this in self:
            if this.date_done:
                this.fecha_letras = this.date_done.strftime("%d de %B de %Y")
            else:
                this.fecha_letras = this.date_done

    def button_validate(self):
        for this in self:
            if this.necesita_aprobacion:
                if this.aprobado:
                    return super(StockPicking, self).button_validate()
                else:
                    raise exceptions.ValidationError(
                        'No puede validar una transferencia sin su debida aprobación')
            else:
                return super(StockPicking, self).button_validate()


    @api.onchange('pedido_materiales_equipos','retiro_materiales_equipos','aprobado')
    @api.depends('pedido_materiales_equipos','retiro_materiales_equipos','aprobado')
    def computeNecesitaAprobacion(self):
        for this in self:
            if this.pedido_materiales_equipos or this.retiro_materiales_equipos:
                if not this.aprobado:
                    this.necesita_aprobacion = True
                else:
                    this.necesita_aprobacion = False
            else:
                this.necesita_aprobacion = False

    @api.onchange('pedido_materiales_equipos', 'retiro_materiales_equipos', 'aprobado')
    @api.depends('pedido_materiales_equipos', 'retiro_materiales_equipos', 'aprobado')
    def computePuedeAprobar(self):
        for this in self:
            if this.picking_type_id.warehouse_id.user_ids:
                context = self._context
                current_uid = context.get('uid')
                if current_uid in this.picking_type_id.warehouse_id.user_ids.ids:
                    this.puede_aprobar = True

    def amount_to_text_esp(self, amount):
        MONEDA_SINGULAR = 'bolivar'
        MONEDA_PLURAL = 'bolivares'

        CENTIMOS_SINGULAR = 'centimo'
        CENTIMOS_PLURAL = 'centimos'

        MAX_NUMERO = 999999999999

        UNIDADES = (
            'cero',
            'uno',
            'dos',
            'tres',
            'cuatro',
            'cinco',
            'seis',
            'siete',
            'ocho',
            'nueve'
        )

        DECENAS = (
            'diez',
            'once',
            'doce',
            'trece',
            'catorce',
            'quince',
            'dieciseis',
            'diecisiete',
            'dieciocho',
            'diecinueve'
        )

        DIEZ_DIEZ = (
            'cero',
            'diez',
            'veinte',
            'treinta',
            'cuarenta',
            'cincuenta',
            'sesenta',
            'setenta',
            'ochenta',
            'noventa'
        )

        CIENTOS = (
            '_',
            'ciento',
            'doscientos',
            'trescientos',
            'cuatroscientos',
            'quinientos',
            'seiscientos',
            'setecientos',
            'ochocientos',
            'novecientos'
        )

        def numero_a_letras(numero):
            numero_entero = int(numero)
            if numero_entero > MAX_NUMERO:
                raise OverflowError('Número demasiado alto')
            if numero_entero < 0:
                return 'menos %s' % numero_a_letras(abs(numero))
            letras_decimal = ''
            parte_decimal = int(
                round((abs(numero) - abs(numero_entero)) * 100))
            if parte_decimal > 9:
                letras_decimal = 'punto %s' % numero_a_letras(parte_decimal)
            elif parte_decimal > 0:
                letras_decimal = 'punto cero %s' % numero_a_letras(
                    parte_decimal)
            if (numero_entero <= 99):
                resultado = leer_decenas(numero_entero)
            elif (numero_entero <= 999):
                resultado = leer_centenas(numero_entero)
            elif (numero_entero <= 999999):
                resultado = leer_miles(numero_entero)
            elif (numero_entero <= 999999999):
                resultado = leer_millones(numero_entero)
            else:
                resultado = leer_millardos(numero_entero)
            resultado = resultado.replace('uno mil', 'un mil')
            resultado = resultado.strip()
            resultado = resultado.replace(' _ ', ' ')
            resultado = resultado.replace('  ', ' ')
            if parte_decimal > 0:
                resultado = '%s %s' % (resultado, letras_decimal)
            return resultado.upper()

        def numero_a_moneda(numero):
            numero_entero = int(numero)
            parte_decimal = int(
                round((abs(numero) - abs(numero_entero)) * 100))
            centimos = ''
            if parte_decimal == 1:
                centimos = CENTIMOS_SINGULAR
            else:
                centimos = CENTIMOS_PLURAL
            moneda = ''
            if numero_entero == 1:
                moneda = MONEDA_SINGULAR
            else:
                moneda = MONEDA_PLURAL
            letras = numero_a_letras(numero_entero)
            letras = letras.replace('uno', 'un')
            letras_decimal = 'con %s %s' % (numero_a_letras(
                parte_decimal).replace('uno', 'un'), centimos)
            letras = '%s %s %s' % (letras, moneda, letras_decimal)
            return letras

        def leer_decenas(numero):
            if numero < 10:
                return UNIDADES[numero]
            decena, unidad = divmod(numero, 10)
            if numero <= 19:
                resultado = DECENAS[unidad]
            elif numero <= 29:
                resultado = 'veinti%s' % UNIDADES[unidad]
            else:
                resultado = DIEZ_DIEZ[decena]
                if unidad > 0:
                    resultado = '%s y %s' % (resultado, UNIDADES[unidad])
            return resultado

        def leer_centenas(numero):
            centena, decena = divmod(numero, 100)
            if numero == 0:
                resultado = 'cien'
            else:
                resultado = CIENTOS[centena]
                if decena > 0:
                    resultado = '%s %s' % (resultado, leer_decenas(decena))
            return resultado

        def leer_miles(numero):
            millar, centena = divmod(numero, 1000)
            resultado = ''
            if (millar == 1):
                resultado = ''
            if (millar >= 2) and (millar <= 9):
                resultado = UNIDADES[millar]
            elif (millar >= 10) and (millar <= 99):
                resultado = leer_decenas(millar)
            elif (millar >= 100) and (millar <= 999):
                resultado = leer_centenas(millar)
            resultado = '%s mil' % resultado
            if centena > 0:
                resultado = '%s %s' % (resultado, leer_centenas(centena))
            return resultado

        def leer_millones(numero):
            millon, millar = divmod(numero, 1000000)
            resultado = ''
            if (millon == 1):
                resultado = ' un millon '
            if (millon >= 2) and (millon <= 9):
                resultado = UNIDADES[millon]
            elif (millon >= 10) and (millon <= 99):
                resultado = leer_decenas(millon)
            elif (millon >= 100) and (millon <= 999):
                resultado = leer_centenas(millon)
            if millon > 1:
                resultado = '%s millones' % resultado
            if (millar > 0) and (millar <= 999):
                resultado = '%s %s' % (resultado, leer_centenas(millar))
            elif (millar >= 1000) and (millar <= 999999):
                resultado = '%s %s' % (resultado, leer_miles(millar))
            return resultado

        def leer_millardos(numero):
            millardo, millon = divmod(numero, 1000000)
            return '%s millones %s' % (leer_miles(millardo), leer_millones(millon))

        convert_amount_in_words = numero_a_letras(amount)
        return convert_amount_in_words
