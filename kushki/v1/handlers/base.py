from .. import exceptions, responses
import requests


class RequestHandler(object):

    def __init__(self, request):
        self._request = request

    def __call__(self):
        try:
            response = requests.post(self._request.url, json=self._request.body, verify=True)
            return responses.Response(response.headers['Content-Type'], response.json(), response.status_code)
        except Exception as e:
            raise exceptions.KushkiException("No se pudo realizar la peticion porque ocurrio un error interno", 3, e)