from . import constants, exceptions
import json
import base64


class Request(object):
    """
    Abstraccion para realizar una peticion al servidor de Kushki.
    """
    # TODO este desarrollo esta incompleto. Verlo bien abajo.

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

        return json.dumps({
            'request': self._encrypted_message_chunk(json.dumps(self.params))
        })

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

        def encrypt(s):
            # TODO hacer bien esta parte con pycrypto.
            return s

        return "".join([base64.b64encode(encrypt(chunk)).replace("\n", "") + "<FS>" for chunk in chunker(plain)])
