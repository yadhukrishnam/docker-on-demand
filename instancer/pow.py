import hashlib
import time

def proof_of_work(block, difficulty):
    """
    Find a nonce that, when hashed with the block data, results in a hash
    with a certain number of leading zeroes.
    """
    target = '0' * difficulty
    for nonce in range(1000000):
        data = f'{block}{nonce}'.encode()
        hash = hashlib.sha256(data).hexdigest()
        if hash[:difficulty] == target:
            return nonce
    return None

block = "skdhfnhgksadfdsjf"
difficulty = 5
start = time.time()
nonce = proof_of_work(block, difficulty)
end = time.time()

if nonce:
    print(f'Proof of work found: {nonce}')
    print(f'Time taken: {end - start} seconds')
    print(f'Hash: {hashlib.sha256((block+str(nonce)).encode()).hexdigest()}')
else:
    print('Proof of work not found')