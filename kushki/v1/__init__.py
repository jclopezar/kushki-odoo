# coding=utf-8
from . import types, exceptions, builders, validators


class Kushki(object):

    def __init__(self, merchant_id, language=types.Languages._default, currency=types.Currencies._default):
        self._merchant_id = merchant_id
        self._language = language
        self._currency = currency

    currency = property(lambda self: self._currency)
    language = property(lambda self: self._language)
    merchant_id = property(lambda self: self._merchant_id)

    def _validate_amount(self, amount):
        """
        Valida la cantidad a pagar, tirando excepciones
        :param amount: Cantidad a pagar
        :return:
        """

        if amount is None:
            raise exceptions.KushkiException(u'El monto no puede ser nulo', 4, amount)
        try:
            amount_ = float(amount)
        except:
            raise exceptions.KushkiException(u'El monto debe ser un valor numérico válido', 5, amount)
        if amount_ < 0:
            raise exceptions.KushkiException(u'El monto debe ser superior a 0')
        formatted_amount = "{0:.2f}".format(amount_)
        if len(formatted_amount) > 12:
            raise exceptions.KushkiException(u'El monto debe tener menos de 12 dígitos')

    def _execute(self, klass, *args):
        """
        Ejecuta una peticion a la API.
        :param klass: Clase de RequestBuilder a usar.
        :param args: Argumentos adicionales.
        :return: El objeto Response obtenido.
        """

        instance = klass(self.merchant_id, *args)
        return instance()

    def charge(self, token, amount):
        """
        Efectiviza un pago.
        :param token: Token a efectivizar.
        :param amount: Valor a comprobar respecto del token efectivo.
        :return: El objeto Response obtenido.
        """

        self._validate_amount(amount)
        return self._execute(builders.ChargeRequestBuilder, token, amount)

    def deferred_charge(self, token, amount, months, interest):
        """
        Efectiviza un pago en cuotas.
        :param token: Token a efectivizar.
        :param amount: Valor a comprobar respecto del token efectivo.
        :param months: Cantidad de meses.
        :param interest: Interes aplicado.
        :return: El objeto Response obtenido.
        """

        self._validate_amount(amount)
        validators.validate_months(months)
        return self._execute(builders.DeferredChargeRequestBuilder, token, amount, months, interest)

    def void_charge(self, ticket, amount):
        """
        Anula un pago.
        :param ticket: El ticket del pago a anular.
        :param amount: El monto del pago a anular.
        :return: El objeto Response obtenido.
        """

        self._validate_amount(amount)
        return self._execute(builders.VoidRequestBuilder, ticket, amount)

    def refund_charge(self, ticket, amount):
        """
        Devuelve un pago.
        :param ticket: El ticket del pago a devolver.
        :param amount: La cantidad a devolver.
        :return: El objeto Response obtenido.
        """

        self._validate_amount(amount)
        return self._execute(builders.RefundRequestBuilder, ticket, amount)

    def request_token(self, card_params):
        """
        Obtiene un token para esos parametros.
        :param card_params: Un diccionario con los parametros de la tarjeta.
        :return: El objeto Response obtenido.
        """

        return self._execute(builders.TokenRequestBuilder, card_params)