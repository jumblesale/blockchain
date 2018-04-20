import hashlib
import sys
import jumblecoin as b

PROOF_COST = 3
TO_FIND = 10


def mine_proofs(previous_proof):
    proofs = []
    i = 0

    while len(proofs) < TO_FIND:
        i += 1
        hex_result = hashlib\
            .sha256(str(i * previous_proof).encode())\
            .hexdigest()
        if hex_result.endswith('0' * PROOF_COST):
            print(i)
            proofs.append(i)
    print(proofs)

    for proof in proofs:
        print(b.validate_proof(proof, previous_proof))


def mine_next(previous_proof):
    i = 0
    previous_proof = int(previous_proof)
    while True:
        i += 1
        hex_result = hashlib\
            .sha256(str(i * previous_proof).encode())\
            .hexdigest()
        if hex_result.endswith('0' * PROOF_COST):
            return i

if __name__ == '__main__':
    mine_next(1)
    mine_proofs(sys.argv[1])
