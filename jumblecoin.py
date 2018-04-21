import time
import hashlib
import typing
import json
from hash import hash_object as hash_block

PROOF_COST = 3


class Block:
    def __init__(self, index: int, timestamp: str, previous_hash: typing.Optional[str], data: str, proof: int):
        self.index = index
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.data = data
        self.proof = proof


class Chain:
    def __init__(self, genesis_block: Block):
        self.blocks = [genesis_block]

    def to_dict(self):
        return {
            'blocks': [b.__dict__ for b in self.blocks]
        }


def _new_block(index: int, previous_hash: typing.Optional[str], data: str, proof: int) -> Block:
    return Block(index, time.time(), previous_hash, data, proof)


def new_chain():
    genesis_block = _new_block(
        index=0, previous_hash=None,
        data=json.dumps({'name': 'jumblesale', 'value': 100}),
        proof=0
    )
    return Chain(genesis_block)


def last_block(chain: Chain) -> Block:
    return chain.blocks[-1]


def add_block_to_chain(chain: Chain, block: Block) -> Chain:
    chain.blocks.append(block)
    return chain


def add_new_block_to_chain(chain: Chain, data: str, proof: int) -> Chain:
    block = _new_block(
        index=len(chain.blocks),
        previous_hash=hash_block(last_block(chain)),
        data=data,
        proof=proof
    )
    return add_block_to_chain(chain, block)


def set_proof_cost(new_cost: int):
    global PROOF_COST
    PROOF_COST = new_cost


def validate_proof(proof: int, previous_proof: int) -> (bool, str):
    hex_result = hashlib \
        .sha256((str(previous_proof) + str(proof)).encode()) \
        .hexdigest()
    return hex_result.endswith('0' * PROOF_COST), hex_result


def validate_block_data_for_chain(chain: Chain, previous_hash, proof, data) -> (bool, [str]):
    errors = []
    last_hash = hash_block(last_block(chain))
    if last_hash != previous_hash:
        errors.append('Previous hash does not match!')
    if type(data) is not str or len(data) == 0:
        errors.append('Data property is empty!')
    last_proof = last_block(chain).proof
    validation_success, hex_result = validate_proof(proof, last_proof)
    if not validation_success:
        errors.append(
            '{} is not a valid proof! sha_256({}{}) = {} - should end in {}'.format(
                proof, proof, last_proof, hex_result, ('0' * PROOF_COST)
            )
        )
    return not errors, errors
