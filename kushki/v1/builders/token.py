from .base import RequestBuilder
from .. import constants


class ChargeRequestBuilder(RequestBuilder):
    """
    Constructor para armar una request relacionada a obtener un token relacionado con la tarjeta en uso.
    """

    def __init__(self, merchant_id, card_params):
        super(ChargeRequestBuilder, self).__init__(merchant_id, constants.TOKENS_URL)
        self._card_name = card_params[constants.PARAMETER_CARD_NAME]
        self._card_number = card_params[constants.PARAMETER_CARD_NUMBER]
        self._card_expiry_month = card_params[constants.PARAMETER_CARD_EXP_MONTH]
        self._card_expiry_year = card_params[constants.PARAMETER_CARD_EXP_YEAR]
        self._card_cvc = card_params[constants.PARAMETER_CARD_CVC]

    def _requestParams(self):
        return {
            constants.PARAMETER_CURRENCY_CODE: self._currency,
            constants.PARAMETER_MERCHANT_ID: self._merchant_id,
            constants.PARAMETER_LANGUAGE: self._language,
            constants.PARAMETER_CARD: {
                constants.PARAMETER_CARD_NAME: self._card_name,
                constants.PARAMETER_CARD_NUMBER: self._card_number,
                constants.PARAMETER_CARD_EXP_MONTH: self._card_expiry_month,
                constants.PARAMETER_CARD_EXP_YEAR: self._card_expiry_year,
                constants.PARAMETER_CARD_CVC: self._card_cvc,
            }
        }
