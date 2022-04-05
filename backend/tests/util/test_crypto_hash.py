from backend.bc_utils.crypto_hash import crypto_hash

def test_crypto_hash():
    assert crypto_hash(1, [2], 'three') != crypto_hash('three', 1, [2]) # It should assert to true if order of arguments does change the hash result.
    assert crypto_hash('foo') == 'b2213295d564916f89a6a42455567c87c3f480fcd7a1c15e220f17d7169a790b'