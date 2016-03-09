from . import constants, exceptions
import json
import base64


from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
# TODO change this later. Currently kushki uses PKCS1 both in php and this implementation (they should use OAEP).
# TODO masking with MGF1 and hashing with SHA1 will be used for PHP if the constant chanes to OAEP setting.
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
            raise exceptions.KushkiException("No se puede encriptar porque el contenido es mas largo que la clave "
                                             "de encriptacion", 1, None)
        except Exception as e:
            raise exceptions.KushkiException("No se puede encriptar porque ocurrio un error interno", 2, e)
