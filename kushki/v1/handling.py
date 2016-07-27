# coding=utf-8
import json
import base64
import requests
from . import constants, exceptions


from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
# TODO change this later. Currently kushki uses PKCS1 both in php and this implementation (they should use OAEP).
# TODO masking with MGF1 and hashing with SHA1 will be used for PHP if the constant changes to OAEP setting.
encrypter = PKCS1_v1_5.new(RSA.importKey(constants.KUSHKI_PUBLIC_KEY))


class Request(object):
    """
    Abstraccion para realizar una peticion al servidor de Kushki.
    """

    def __init__(self, url, params, content_type=constants.CONTENT_TYPE):
        self._url = url
        self._params = params
        self._content_type = content_type

    url = property(lambda self: self._url)
    params = property(lambda self: self._params)
    content_type = property(lambda self: self._content_type)

    def param(self, param_name):
        """
        Obtiene un parametro de la request.
        :param param_name: nombre del parametro a obtener.
        :return:
        """

        try:
            return self.params[param_name]
        except KeyError:
            raise exceptions.KushkiException(constants.PARAMETER_DO_NOT_EXIST)

    @property
    def body(self):
        """
        Arma el cuerpo de la peticion, encriptando su contenido.
        :return:
        """

        return {
            'request': self._encrypted_message_chunk(json.dumps(self.params))
        }

    @staticmethod
    def _encrypted_message_chunk(plain):
        """
        Obtiene el cuerpo encriptado.
        :param plain:
        :return:
        """

        def chunker(s):
            for idx in range(0, len(s), 117):
                yield s[idx:idx+117]
        try:
            return "".join([base64.b64encode(encrypter.encrypt(chunk)).replace("\n", "") + "<FS>"
                            for chunk in chunker(plain)])
        except ValueError:
            raise exceptions.KushkiException(u"No se puede encriptar porque el contenido es más largo que la clave "
                                             u"de encriptación", 1, None)
        except Exception as e:
            raise exceptions.KushkiException(u"No se puede encriptar porque ocurrió un error interno", 2, e)


class Response(object):
    """
    Abstraccion para armar una respuesta recibida desde el backend de Kushki.
    """

    def __init__(self, content_type, body, code):
        self._content_type = content_type
        self._body = body
        self._code = code

    content_type = property(lambda self: self._content_type)
    body = property(lambda self: self._body)
    code = property(lambda self: self._code)
    successful = property(lambda self: self._code == 200)
    token = property(lambda self: self._body['transaction_token'])
    ticket_number = property(lambda self: self._body['ticket_number'])
    approved_amount = property(lambda self: self._body['approved_amount'])
    response_code = property(lambda self: self._body['response_code'])
    response_text = property(lambda self: self._body['response_text'])


class RequestHandler(object):

    def __init__(self, request):
        self._request = request

    def __call__(self):
        try:
            response = requests.post(self._request.url, json=self._request.body, verify=True)
            return Response(response.headers['Content-Type'], response.json(), response.status_code)
        except Exception as e:
            raise exceptions.KushkiException(u"No se pudo realizar la petición porque ocurrió un error interno", 3, e)