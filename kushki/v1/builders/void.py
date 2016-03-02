from .base import RequestBuilder
from .. import constants


class RefundRequestBuilder(RequestBuilder):
    """
    Constructor para armar una request relacionada a anular un pago mediante su ticket y su cantidad.
    El pago puede devolverse parcial o totalmente.
    """

    def __init__(self, merchant_id, ticket, amount):
        super(RefundRequestBuilder, self).__init__(merchant_id, constants.VOID_URL)
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


