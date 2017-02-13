from binascii import hexlify, unhexlify


def ensure_bytes(s):
    if not isinstance(s, bytes):
        s = s.encode('utf-8')
    return s


def ensure_unicode(s):
    if isinstance(s, bytes):
        s = s.decode('utf-8')
    return s


def bytes_to_hex(bytestr):
    return hexlify(bytestr).decode('ascii')


def hex_to_bytes(hexed):
    if len(hexed) & 1:
        hexed = u'0' + hexed
    return unhexlify(hexed)
