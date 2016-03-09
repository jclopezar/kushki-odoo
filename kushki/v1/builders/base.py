from ..enums import Currencies, Languages
from ..handling import Request
from ..constants import CONTENT_TYPE


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
        return Request(self._url, self._requestParams(), CONTENT_TYPE)