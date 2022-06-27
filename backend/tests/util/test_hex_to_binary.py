from backend.bc_utils.hex_to_binary import hex_to_binary


def test_hex_to_binary():
    org_num = 908
    hex_num = hex(org_num)
    binary_num = hex_to_binary(hex_num)

    assert int(binary_num,2) == org_num