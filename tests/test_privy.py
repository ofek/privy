import pytest

import privy


class TestPrivy:
    def test_default(self):
        secret = b'secret'
        password = b'password'

        assert privy.peek(privy.hide(secret, password), password) == secret
