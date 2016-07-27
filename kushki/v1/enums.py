from collections import namedtuple


class Languages(object):
    ES = 'es'
    EN = 'en'
    _default = ES


class Currencies(object):
    USD = 'usd'
    _default = USD


KushkiEnvironment = namedtuple('KushkiEnvironment', ('label', 'url'))


class Environments(object):
    TESTING = KushkiEnvironment('PRODUCTION', 'https://uat.aurusinc.com/kushki/api/v1')
    STAGING = KushkiEnvironment('STAGING', 'https://staging.aurusinc.com/kushki/api/v1')
    PRODUCTION = KushkiEnvironment('PRODUCTION', 'https://p1.kushkipagos.com/kushki/api/v1')
