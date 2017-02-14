Privy: Secrets made easy
========================

.. image:: https://img.shields.io/pypi/v/privy.svg?style=flat-square
    :target: https://pypi.org/project/privy

.. image:: https://img.shields.io/travis/ofek/privy.svg?branch=master&style=flat-square
    :target: https://travis-ci.org/ofek/privy

.. image:: https://img.shields.io/codecov/c/github/ofek/privy.svg?style=flat-square
    :target: https://codecov.io/gh/ofek/privy

.. image:: https://img.shields.io/pypi/pyversions/privy.svg?style=flat-square
    :target: https://pypi.org/project/privy

.. image:: https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square
    :target: https://en.wikipedia.org/wiki/MIT_License

-----

Privy is a small and fast utility for password-protecting secrets such as
seeds for digital signatures or Bitcoin wallets.

Usage
-----

.. code-block:: python

    >>> import privy
    >>>
    >>> secret = b'secret'
    >>> password = 'foo'
    >>>
    >>> hidden = privy.hide(secret, password)
    >>> hidden
    '1$2$c016b66bd5...'
    >>>
    >>> privy.peek(hidden, password)
    b'secret'

Installation
------------

Privy is available on Linux/macOS and Windows and supports Python 2.7, 3.4+, and PyPy.

.. code-block:: bash

    $ pip install privy

Encryption scheme
-----------------

Secrets are encrypted using the `Fernet`_ protocol. Specifically, it uses AES for
encryption and has built-in authentication using HMAC. The private key used for
encryption is derived from the password using a `key derivation function`_. The
key derivation function used is `Argon2`_, the winner of the `Password Hashing
Competition`_. Both Argon2i and Argon2d variants are supported.

Secrets encrypted with default settings are unicode strings of length 269.

API
---

There are 2 functions: ``hide`` and ``peek``.

hide(secret, password, security=2, salt=None, server=True)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Encrypts ``secret`` using ``password``. Returns the hidden secret as unicode.

* Parameters

  - **secret** (``bytes``) - The secret to encrypt.
  - **password** (``bytes`` or ``unicode``) - The password used to access the secret.
  - **security** (``int``) - A number 0-10 inclusive. Higher values are more secure at
    the cost of slower computation and greater use of memory. See `security levels`_.
  - **salt** (``bytes``) - The salt used for the password hash. Defaults to ``os.urandom(32)``.
  - **server** (``bool``) - If ``True``, it is assumed side-channel attack protection is
    needed and therefore the Argon2i algorithm will be used. Otherwise, the password will
    be hashed using the Argon2d algorithm.

peek(hidden, password, expires=None)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Decrypts ``hidden`` using ``password``. Returns the secret as ``bytes``.

* Parameters

  - **hidden** (``bytes`` or ``unicode``) - The hidden secret to decrypt.
  - **password** (``bytes`` or ``unicode``) - The password used to access the secret.
  - **expires** (``int``) - The maximum number of seconds since encryption that
    is allowed. The default is no expiration.

A ``ValueError`` will be raised if the password is wrong, the password was attempted on a
different hidden secret, or the number of seconds since encryption is > ``expires`` argument.

Security levels
---------------

All expected times were taken from tests on an Intel Core i7-2670QM @ 2.2 GHz.

+--------+-----------------+---------------+-----------------+
| Levels | Argon2 settings | Expected time | Notes           |
+========+=================+===============+=================+
| 0      | m=8 KiB, t=1    | 600 usec      | Lowest possible |
+--------+-----------------+---------------+-----------------+
| 1      | m=4 MiB, t=10   | 50 msec       |                 |
+--------+-----------------+---------------+-----------------+
| 2      | m=8 MiB, t=10   | 100 msec      | Default         |
+--------+-----------------+---------------+-----------------+
| 3      | m=32 MiB, t=10  | 350 msec      |                 |
+--------+-----------------+---------------+-----------------+
| 4      | m=48 MiB, t=10  | 550 msec      |                 |
+--------+-----------------+---------------+-----------------+
| 5      | m=96 MiB, t=10  | 1.1 sec       | Good choice     |
+--------+-----------------+---------------+-----------------+
| 6      | m=256 MiB, t=10 | 3 sec         |                 |
+--------+-----------------+---------------+-----------------+
| 7      | m=448 MiB, t=10 | 5.3 sec       |                 |
+--------+-----------------+---------------+-----------------+
| 8      | m=768 MiB, t=10 | 9.1 sec       |                 |
+--------+-----------------+---------------+-----------------+
| 9      | m=1 GiB, t=10   | 12.2 sec      |                 |
+--------+-----------------+---------------+-----------------+
| 10     | m=2 GiB, t=20   | 48 sec        | Lots of RAM     |
+--------+-----------------+---------------+-----------------+


.. _Fernet: https://github.com/fernet/spec/blob/master/Spec.md
.. _key derivation function: https://en.wikipedia.org/wiki/Key_derivation_function
.. _Argon2: https://github.com/p-h-c/phc-winner-argon2
.. _Password Hashing Competition: https://en.wikipedia.org/wiki/Password_Hashing_Competition
.. _security levels: https://github.com/ofek/privy#security-levels
