import time

import pytest

import privy


def test_default():
    secret = b'secret'
    password = b'password'

    hidden = privy.hide(secret, password)

    assert privy.peek(hidden, password) == secret


def test_security():
    secret = b'secret'
    password = b'password'

    hidden = privy.hide(secret, password, security=3)

    assert privy.peek(hidden, password) == secret


def test_invalid_security():
    secret = b'secret'
    password = b'password'

    with pytest.raises(KeyError):
        privy.hide(secret, password, security=99)


def test_salt():
    secret = b'secret'
    password = b'password'

    hidden = privy.hide(secret, password, salt=b'bad_form')

    assert privy.peek(hidden, password) == secret


def test_no_server():
    secret = b'secret'
    password = b'password'

    hidden = privy.hide(secret, password, server=False)

    assert privy.peek(hidden, password) == secret


def test_unicode_password():
    secret = b'secret'
    password = u'password'

    hidden = privy.hide(secret, password)

    assert privy.peek(hidden, password) == secret


def test_peek_non_unicode_hidden():
    secret = b'secret'
    password = b'password'

    hidden = privy.hide(secret, password).encode('utf-8')

    assert privy.peek(hidden, password) == secret


def test_wrong_password():
    secret = b'secret'
    password = b'password'

    hidden = privy.hide(secret, password)

    with pytest.raises(ValueError):
        privy.peek(hidden, b'wrong')


def test_wrong_hidden_secret():
    secret = b'secret'
    password = b'password'

    hidden = privy.hide(secret, b'wrong')

    with pytest.raises(ValueError):
        privy.peek(hidden, password)


def test_expires():
    secret = b'secret'
    password = b'password'

    hidden = privy.hide(secret, password)
    time.sleep(2)

    with pytest.raises(ValueError):
        privy.peek(hidden, password, expires=1)
