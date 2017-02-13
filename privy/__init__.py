from base64 import urlsafe_b64encode
from collections import OrderedDict
from os import urandom

from argon2.low_level import Type, hash_secret_raw
from cryptography.fernet import Fernet

from .utils import bytes_to_hex, hex_to_bytes


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
    (7, {'memory_cost': MB * 448, 'time_cost': 10}),
    (8, {'memory_cost': MB * 768, 'time_cost': 10}),
    (9, {'memory_cost': MB * MB, 'time_cost': 10}),
    (10, {'memory_cost': MB * MB * 2, 'time_cost': 20}),
])

SECURITY_LEVEL_TIMES = OrderedDict([
    (0, 0.0005),
    (1, 0.05),
    (2, 0.09),
    (3, 0.35),
    (4, 0.55),
    (5, 1),
    (6, 3),
    (7, 5),
    (8, 9),
    (9, 12),
    (10, 48),
])


def hide(secret, password, security=2, salt=None, server=True):
    salt = salt or urandom(SALT_LENGTH)

    hashed = hash_secret_raw(
        password, salt, hash_len=HASH_LENGTH, parallelism=THREADS,
        type=Type.I if server else Type.D, **SECURITY_LEVELS[security]
    )

    token = Fernet(urlsafe_b64encode(hashed)).encrypt(secret)

    return u'{}${}${}${}'.format(
        int(server), security, bytes_to_hex(salt), bytes_to_hex(token)
    )


def peek(hidden, password):
    server, security, salt, token = hidden.split('$')
    server = int(server)
    security = int(security)
    salt = hex_to_bytes(salt)
    token = hex_to_bytes(token)

    hashed = hash_secret_raw(
        password, salt, hash_len=HASH_LENGTH, parallelism=THREADS,
        type=Type.I if server else Type.D, **SECURITY_LEVELS[security]
    )

    return Fernet(urlsafe_b64encode(hashed)).decrypt(token)














