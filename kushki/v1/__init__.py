# coding=utf-8
from . import enums, exceptions


class Kushki(object):

    def __init__(self, merchant_id, language=enums.Languages._default, currency=enums.Currencies._default):
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
        :return: el objeto Response obtenido.
        """
        instance = klass(self.merchant_id, *args)
        return instance()