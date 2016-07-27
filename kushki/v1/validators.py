# coding=utf-8
from . import exceptions
from sys import version_info

PY3 = version_info[0] == 3
PY2 = version_info[0] == 2

def get_string_value(number):
    if isinstance(number, float):
        return "{0:.2f}".format(number)
    elif isinstance(number, int) or PY2 and isinstance(number, long):
        return str(int)
    else:
        return ''

def validate_number(value, min_value, max_length, description):
    if value is None:
        raise exceptions.KushkiException('%s no puede ser un valor nulo' % description)
    if value < min_value:
        raise exceptions.KushkiException('%s debe ser superior o igual a %s' % (description, min_value))
    cleaned = get_string_value(value)
    if len(cleaned) > max_length:
        raise exceptions.KushkiException('%s debe tener %s o menos dígitos' % (description, max_length))
    return cleaned

def validate_months(value):
    return validate_number(value, 0, 2, 'El número de meses')

