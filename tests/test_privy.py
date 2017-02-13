import pytest

import privy


class TestPrivy:
    def test_default(self):
        secret = b'secret'
        password = b'password'

        hidden = privy.hide(secret, password)

        assert privy.peek(hidden, password) == secret

    def test_unicode_password(self):
        secret = b'secret'
        password = u'password'

        hidden = privy.hide(secret, password)

        assert privy.peek(hidden, password) == secret
