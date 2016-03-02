from .base import RequestBuilder
from .. import constants


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
