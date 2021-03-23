import sys
from hashlib import blake2b
from random import Random
from secrets import SystemRandom, token_bytes

"""
See: https://en.wikipedia.org/wiki/Random_oracle
"""
class RandomOracle(object):

    def __init__(self,
            salt=None,
            person=None,
            key=None,
            seed=None,
            mod_size=sys.maxsize,
            hash_digest_size=32):

        # Random() can be seeded for reproducability but should not be used in
        # real world applications.
        self._random = SystemRandom() if seed is None else Random(seed)

        # Number of bits used for quadratic function moduli
        self._mod_size = mod_size

        # Blake2b params
        self._salt = salt.to_bytes(length=16, byteorder='big') if salt else b''
        self._person = person.to_bytes(length=16, byteorder='big') if person else b''
        self._key = key.to_bytes(length=16, byteorder='big') if key else b''
        self._hash_digest_size = min(blake2b.MAX_DIGEST_SIZE, hash_digest_size)

        # Storage for oracles
        self._mapping = {}


    # Stores and returns the output of a randomly generated quadratic function
    # applied to input i
    def oracle(self, i):
        if i not in self._mapping:
            # Pick 3 large random integers
            x, y, z = list(self._random.choices(range(1, self._mod_size), k=3))
            # Use them to construct a quadratic function
            f = lambda a: ((x*(a+1))**2)+(y*(a+1))+z
            # Apply it to i and store the output
            self._mapping[i] = f(i)

        return self._mapping[i]


    def hash(self, i):
        oracle = self.oracle(i).to_bytes(self._hash_digest_size, byteorder='big')
        h = blake2b(oracle, salt=self._salt, person=self._person, key=self._key,
                digest_size=self._hash_digest_size)
        return h.hexdigest()


if __name__ == '__main__':
    oracle = RandomOracle(1)
    [print(f'i={str(i).zfill(2)}, o={oracle.oracle(i)}, hash={oracle.hash(i)}')
        for i in range(0,10)]
