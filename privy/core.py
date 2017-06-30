from base64 import urlsafe_b64encode
from collections import OrderedDict
from os import urandom

from argon2.low_level import Type, hash_secret_raw
from cryptography.fernet import Fernet, InvalidToken

from .utils import base64_to_bytes, bytes_to_base64, ensure_bytes, ensure_unicode


HASH_LENGTH = 32
SALT_LENGTH = 32
THREADS = 1

MB = 1024

SECURITY_LEVELS = OrderedDict([
    (0, {'memory_cost': 8, 'time_cost': 1}),
    (1, {'memory_cost': MB * 4, 'time_cost': 10}),
    (2, {'memory_cost': MB * 8, 'time_cost': 10}),
    (3, {'memory_cost': MB * 32, 'time_cost': 10}),
    (4, {'memory_cost': MB * 48, 'time_cost': 10}),
    (5, {'memory_cost': MB * 96, 'time_cost': 10}),
    (6, {'memory_cost': MB * 256, 'time_cost': 10}),
    (7, {'memory_cost': MB * 512, 'time_cost': 10}),
    (8, {'memory_cost': MB * 768, 'time_cost': 10}),
    (9, {'memory_cost': MB * MB, 'time_cost': 10}),
    (10, {'memory_cost': MB * MB * 2, 'time_cost': 20}),
    (11, {'memory_cost': MB * MB * 3, 'time_cost': 30}),
    (12, {'memory_cost': MB * MB * 4, 'time_cost': 40}),
    (13, {'memory_cost': MB * MB * 5, 'time_cost': 50}),
    (14, {'memory_cost': MB * MB * 6, 'time_cost': 60}),
    (15, {'memory_cost': MB * MB * 7, 'time_cost': 70}),
    (16, {'memory_cost': MB * MB * 8, 'time_cost': 80}),
    (17, {'memory_cost': MB * MB * 9, 'time_cost': 90}),
    (18, {'memory_cost': MB * MB * 10, 'time_cost': 100}),
    (19, {'memory_cost': MB * MB * 11, 'time_cost': 110}),
    (20, {'memory_cost': MB * MB * 12, 'time_cost': 120}),
])


def hide(secret, password, security=2, salt=None, server=True):
    password = ensure_bytes(password)

    salt = salt or urandom(SALT_LENGTH)

    hashed = hash_secret_raw(
        password, salt, hash_len=HASH_LENGTH, parallelism=THREADS,
        type=Type.I if server else Type.D, **SECURITY_LEVELS[security]
    )

    token = Fernet(urlsafe_b64encode(hashed)).encrypt(secret)

    return u'{}${}${}${}'.format(
        int(server), security, bytes_to_base64(salt), bytes_to_base64(token)
    )


def peek(hidden, password, expires=None):
    password = ensure_bytes(password)

    server, security, salt, token = ensure_unicode(hidden).split('$')
    server = int(server)
    security = int(security)
    salt = base64_to_bytes(ensure_bytes(salt))
    token = base64_to_bytes(ensure_bytes(token))

    hashed = hash_secret_raw(
        password, salt, hash_len=HASH_LENGTH, parallelism=THREADS,
        type=Type.I if server else Type.D, **SECURITY_LEVELS[security]
    )

    try:
        secret = Fernet(urlsafe_b64encode(hashed)).decrypt(token, expires)
    except InvalidToken:
        raise ValueError(
            'Unable to decrypt secret. The means either the password is wrong,'
            ' the password was attempted on a different hidden secret, or the '
            'secret was encrypted more than {} seconds ago.'.format(expires)
        )

    return secret
