import argparse
import re

SIZES = dict(
    c   = 1,
    w   = 1 << 1,
    b   = 1 << 9,
    kB  = 10 ** 3,
    K   = 1 << 10,
    MB  = 10 ** 6,
    M   = 1 << 20,
    xM  = 1 << 20,
    GB  = 10 ** 9,
    G   = 1 << 30,
    TB  = 10 ** 12,
    T   = 1 << 40,
    PB  = 10 ** 15,
    P   = 1 << 50,
    EB  = 10 ** 18,
    E   = 1 << 60,
    ZB  = 10 ** 21,
    Z   = 1 << 70,
    YB  = 10 ** 24,
    Y   = 1 << 80,
)

BYTE_STRING_REGEX = re.compile('^(\d+)({})$'.format('|'.join(SIZES.keys())))

class DeHumanizeAction(argparse.Action):

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError('nargs is not allowed.')
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        value = dehumanize_byte_string(values)
        setattr(namespace, self.dest, value)

def dehumanize_byte_string(byte_string : str) -> int:
    if byte_string.isdigit():
        return int(byte_string)
    m = BYTE_STRING_REGEX.match(byte_string)
    if m is None:
        raise ValueError('Unsupported format')
    return int(m.group(1)) * SIZES[m.group(2)]