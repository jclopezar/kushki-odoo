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
