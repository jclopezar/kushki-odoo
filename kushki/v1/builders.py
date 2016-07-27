from .types import Currencies, Languages
from .handling import Request
from . import constants


class RequestBuilder(object):
    """
    Constructor para armar una request lista para ser ejecutada. Debe definirse exactamente
      que es lo que construye el metodo _requestParams asi se arma correctamente la request
      a ser enviada.
    """

    def __init__(self, merchant_id, url):
        self._url = url
        self._merchant_id = merchant_id
        self._currency = Currencies._default
        self._language = Languages._default

    def _requestParams(self):
        raise NotImplementedError

    def _createRequest(self):
        return Request(self._url, self._requestParams(), constants.CONTENT_TYPE)


class ChargeRequestBuilder(RequestBuilder):
    """
    Constructor para armar una request relacionada a efectivizar un pago mediante su token y su cantidad.
    """

    def __init__(self, merchant_id, token, amount):
        super(ChargeRequestBuilder, self).__init__(merchant_id, constants.CHARGE_URL)
        self._token = token
        self._amount = amount

    def _requestParams(self):
        return {
            constants.PARAMETER_TRANSACTION_TOKEN: self._token,
            constants.PARAMETER_TRANSACTION_AMOUNT: self._amount,
            constants.PARAMETER_CURRENCY_CODE: self._currency,
            constants.PARAMETER_MERCHANT_ID: self._merchant_id,
            constants.PARAMETER_LANGUAGE: self._language
        }


class DeferredChargeRequestBuilder(RequestBuilder):
    """
    Constructor para armar una request relacionada a efectivizar un pago en cuotas mediante su monto y token.
    """

    def __init__(self, merchant_id, token, amount, months, interest):
        super(DeferredChargeRequestBuilder, self).__init__(merchant_id, constants.DEFERRED_URL)
        self._token = token
        self._amount = amount
        self._months = months
        self._interest = interest

    def _requestParams(self):
        return {
            constants.PARAMETER_TRANSACTION_TOKEN: self._token,
            constants.PARAMETER_TRANSACTION_AMOUNT: self._amount,
            constants.PARAMETER_MONTHS: self._months,
            constants.PARAMETER_INTEREST: self._interest,
            constants.PARAMETER_CURRENCY_CODE: self._currency,
            constants.PARAMETER_MERCHANT_ID: self._merchant_id,
            constants.PARAMETER_LANGUAGE: self._language
        }

# NOT SUPPORTED ANYMORE
#
# class RefundRequestBuilder(RequestBuilder):
#     """
#     Constructor para armar una request relacionada a devolver un pago mediante su ticket y su cantidad.
#     El pago puede devolverse parcial o totalmente.
#     """
#
#     def __init__(self, merchant_id, ticket, amount):
#         super(RefundRequestBuilder, self).__init__(merchant_id, constants.REFUND_URL)
#         self._ticket = ticket
#         self._amount = amount
#
#     def _requestParams(self):
#         return {
#             constants.PARAMETER_TRANSACTION_TICKET: self._ticket,
#             constants.PARAMETER_TRANSACTION_AMOUNT: self._amount,
#             constants.PARAMETER_CURRENCY_CODE: self._currency,
#             constants.PARAMETER_MERCHANT_ID: self._merchant_id,
#             constants.PARAMETER_LANGUAGE: self._language
#         }


class TokenRequestBuilder(RequestBuilder):
    """
    Constructor para armar una request relacionada a obtener un token relacionado con la tarjeta en uso.
    """

    def __init__(self, merchant_id, card_params, remember_me='0'):
        super(TokenRequestBuilder, self).__init__(merchant_id, constants.TOKENS_URL)
        self._card_name = card_params[constants.PARAMETER_CARD_NAME]
        self._card_number = card_params[constants.PARAMETER_CARD_NUMBER]
        self._card_expiry_month = card_params[constants.PARAMETER_CARD_EXP_MONTH]
        self._card_expiry_year = card_params[constants.PARAMETER_CARD_EXP_YEAR]
        self._card_cvc = card_params[constants.PARAMETER_CARD_CVC]
        self._remember_me = remember_me

    def _requestParams(self):
        return {
            constants.PARAMETER_CURRENCY_CODE: self._currency,
            constants.PARAMETER_MERCHANT_ID: self._merchant_id,
            constants.PARAMETER_LANGUAGE: self._language,
            constants.PARAMETER_REMEMBER_ME: self._remember_me,
            constants.PARAMETER_CARD: {
                constants.PARAMETER_CARD_NAME: self._card_name,
                constants.PARAMETER_CARD_NUMBER: self._card_number,
                constants.PARAMETER_CARD_EXP_MONTH: self._card_expiry_month,
                constants.PARAMETER_CARD_EXP_YEAR: self._card_expiry_year,
                constants.PARAMETER_CARD_CVC: self._card_cvc,
            }
        }


class VoidRequestBuilder(RequestBuilder):
    """
    Constructor para armar una request relacionada a anular un pago mediante su ticket y su cantidad.
    El pago puede devolverse parcial o totalmente.
    """

    def __init__(self, merchant_id, ticket, amount):
        super(VoidRequestBuilder, self).__init__(merchant_id, constants.VOID_URL)
        self._ticket = ticket
        self._amount = amount

    def _requestParams(self):
        return {
            constants.PARAMETER_TRANSACTION_TICKET: self._ticket,
            constants.PARAMETER_TRANSACTION_AMOUNT: self._amount,
            constants.PARAMETER_CURRENCY_CODE: self._currency,
            constants.PARAMETER_MERCHANT_ID: self._merchant_id,
            constants.PARAMETER_LANGUAGE: self._language
        }