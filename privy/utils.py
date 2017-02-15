from base64 import urlsafe_b64decode, urlsafe_b64encode


def base64_to_bytes(s):
    return urlsafe_b64decode(s)


def bytes_to_base64(s):
    return urlsafe_b64encode(s).decode('ascii')


def ensure_bytes(s):
    if not isinstance(s, bytes):
        s = s.encode('utf-8')
    return s


def ensure_unicode(s):
    if isinstance(s, bytes):
        s = s.decode('utf-8')
    return s
