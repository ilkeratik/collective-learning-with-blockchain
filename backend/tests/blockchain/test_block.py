import pytest
from backend.blockchain.block import Block, GENESIS_DATA
from backend.config import MINE_RATE, SECONDS
from backend.bc_utils.hex_to_binary import hex_to_binary
import time

def test_mine_block():
    last_block = Block.genesis()
    data = 'test-data'
    block = Block.mine_block(last_block, data)

    assert isinstance(block, Block)
    assert block.data == data
    assert block.last_hash == last_block.hash
    assert hex_to_binary(block.hash)[0:block.difficulty] == '0' * block.difficulty

def test_genesis():
    genesis = Block.genesis()

    assert isinstance(genesis, Block)
    
    for key, value in GENESIS_DATA.items():
        assert getattr(genesis, key) == value

def test_quickly_mined_block():
    last_block = Block.mine_block(Block.genesis(), 'foo')
    mined_block = Block.mine_block(last_block, 'ilker')
    
    assert mined_block.difficulty == last_block.difficulty +1

def test_slowly_mined_block():
    last_block = Block.mine_block(Block.genesis(), 'foo')

    time.sleep(MINE_RATE/ SECONDS)
    mined_block = Block.mine_block(last_block, 'ilker')

    assert mined_block.difficulty == (last_block.difficulty)-1

def test_mined_block_difficulty_limit_at_1():
    last_block = Block(
        time.time_ns(),
        'test_last_hash',
        'test_hash',
        'test_data',
        1,0
    ) # Difficulty is 1 in this block
    time.sleep(MINE_RATE/ SECONDS) #waiting for spending time to pass mine_rate
    mined_block = Block.mine_block(last_block, 'ilker')
    
    assert mined_block.difficulty == 1 # even though the mining took longer than mine_rate, adjust_difficulty func doesn't decrease the difficulty, assuring difficulty to be at least 1. 

@pytest.fixture
def last_block():
    return Block.genesis()

@pytest.fixture
def block(last_block):
    return Block.mine_block(last_block, 'test')

def test_is_valid_block(last_block, block):
    Block.is_valid_block(last_block, block)

def test_is_valid_block_bad_last_hash(last_block, block):
    block.last_hash = 'changeeedd'

    with pytest.raises(Exception, match='last_hash must be correct'): 
        Block.is_valid_block(last_block,block)

def test_is_valid_block_bad_PoW(last_block, block):
    block.hash = 'ffff'

    with pytest.raises(Exception, match='PoW requirement was not meet'): 
        Block.is_valid_block(last_block,block)

def test_is_valid_block_jumped_difficulty(last_block, block):
    diff = 10
    block.difficulty = diff
    block.hash = f'{"0"*diff}12acc'

    with pytest.raises(Exception, match='The block difficulty must only adjust by 1'): 
        Block.is_valid_block(last_block,block)

def test_is_valid_block_bad_block_hash(last_block, block):
    block.hash = '0'*20 + 'abababc'

    with pytest.raises(Exception, match='The block hash must be correct'): 
        Block.is_valid_block(last_block,block)