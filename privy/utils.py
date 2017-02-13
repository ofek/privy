from binascii import hexlify, unhexlify


def bytes_to_hex(bytestr):
    return hexlify(bytestr).decode('ascii')


def hex_to_bytes(hexed):
    if len(hexed) & 1:
        hexed = u'0' + hexed
    return unhexlify(hexed)
