from privy.utils import bytes_to_hex, hex_to_bytes


BYTES = b'TH8\xe2\xaaN\xd7^aX7\x93\xe7\xc6\xa3\x02\x85'
HEX = u'544838e2aa4ed75e61583793e7c6a30285'
ODD_HEX = u'4fadd1977328c11efc1c1d8a781aa6b9677984d3e0bd0bfc52b9f3b03885a00'
ODD_HEX_BYTES = (b'\x04\xfa\xdd\x19w2\x8c\x11\xef\xc1\xc1\xd8\xa7\x81'
                 b'\xaak\x96w\x98M>\x0b\xd0\xbf\xc5+\x9f;\x03\x88Z\x00')


def test_bytes_to_hex():
    assert bytes_to_hex(BYTES) == HEX


def test_hex_to_bytes():
    assert hex_to_bytes(HEX) == BYTES
    assert hex_to_bytes(ODD_HEX) == ODD_HEX_BYTES
