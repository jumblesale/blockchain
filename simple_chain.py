import typing
import time
from hash import hash_object as hash_block


class Block:
    def __init__(self, index: int, timestamp: str, previous_hash: typing.Optional[str], data: str):
        self.index = index
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.data = data


class Chain:
    def __init__(self, genesis_block: Block):
        self.blocks = [genesis_block]

    def to_dict(self):
        return {
            'blocks': [b.__dict__ for b in self.blocks]
        }


def new_chain() -> Chain:
    genesis_block = _new_block(0, None, 'genesis block')
    return Chain(genesis_block)


def _new_block(index: int, previous_hash: typing.Optional[str], data: str) -> Block:
    return Block(index, time.time(), previous_hash, data)


def add_new_block_to_chain(chain: Chain, previous_hash: str, data: str) -> Chain:
    block = _new_block(
        index=len(chain.blocks),
        previous_hash=previous_hash,
        data=data
    )
    return add_block_to_chain(chain, block)


def last_block(chain: Chain) -> Block:
    return chain.blocks[-1]


def next_previous_hash(chain: Chain) -> str:
    return hash_block(last_block(chain))


def add_block_to_chain(chain: Chain, block: Block) -> Chain:
    chain.blocks.append(block)
    return chain
