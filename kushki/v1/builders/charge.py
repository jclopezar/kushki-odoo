from .base import RequestBuilder
from .. import constants


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
