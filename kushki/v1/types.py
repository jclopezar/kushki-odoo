from collections import namedtuple
from . import validators


class Languages(object):
    ES = 'es'
    EN = 'en'
    _default = ES


class Currencies(object):
    USD = 'usd'
    _default = USD


KushkiEnvironment = namedtuple('KushkiEnvironment', ('label', 'url'))


class Environments(object):
    TESTING = KushkiEnvironment('PRODUCTION', 'https://uat.aurusinc.com/kushki/api/v1')
    STAGING = KushkiEnvironment('STAGING', 'https://staging.aurusinc.com/kushki/api/v1')
    PRODUCTION = KushkiEnvironment('PRODUCTION', 'https://p1.kushkipagos.com/kushki/api/v1')


class Amount(namedtuple('Amount', ('subtotal_iva', 'iva', 'subtotal_iva_0', 'ice'))):

    def to_hash(self):
        """
        Valida y devuelve un diccionario con las claves.
        :return:
        """

        subtotal_iva = validators.validate_number(self.subtotal_iva, 0, 12, 'El subtotal IVA')
        subtotal_iva_0 = validators.validate_number(self.subtotal_iva_0, 0, 12, 'El subtotal IVA 0')
        iva = validators.validate_number(self.iva, 0, 12, 'El IVA')
        ice = validators.validate_number(self.ice, 0, 12, 'El ICE')
        total = self.subtotal_iva + self.subtotal_iva_0 + self.iva + self.ice
        return {
            'Subtotal_IVA': subtotal_iva,
            'Subtotal_IVA0': subtotal_iva_0,
            'IVA': iva,
            'ICE': ice,
            'Total_amount': total,
        }
