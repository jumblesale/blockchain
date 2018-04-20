import json
import hashlib


def hash_object(block: object) -> str:
    block_string = json.dumps(block.__dict__, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()
