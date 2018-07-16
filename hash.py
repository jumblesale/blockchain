import json
import hashlib
import log


def hash_object(block: object) -> str:
    block_string = json.dumps(block.__dict__, sort_keys=True, separators=(',', ':'))
    log.log(str(block_string))
    return hash_string(block_string)


def hash_string(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()
