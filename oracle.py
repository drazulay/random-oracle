from hashlib import blake2b
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
            mod_size=16,
            digest_size=32):

        self._mapping = {}

        self._random = SystemRandom()

        # Use a 4096bit number as seed if is is None
        if seed is None:
            seed = self._random.getrandbits(4096)

        self._random.seed(seed)

        # Blake2b params
        self._salt = salt
        self._person = person
        self._key = key
        self._digest_size = digest_size
        
        # Random quadratic function used to generate Blake2b input data
        x = self._random.getrandbits(mod_size)
        y = self._random.getrandbits(mod_size)
        beta = self._random.getrandbits(mod_size)
        self._q = lambda i: (x*(i**2))+(y*i)+beta

    def hash(self, i):
        if i not in self._mapping:
            # Calculate a Blake2b hash using random quadratic function
            # function that incorporates i
            self._mapping[i] = blake2b(
                    token_bytes(self._q(i)),
                    salt=self._salt if self._salt is not None else token_bytes(16),
                    person=self._person if self._person is not None else token_bytes(16),
                    key=self._key if self._key is not None else token_bytes(64),
                    digest_size=self._digest_size).hexdigest()

        return self._mapping[i]

if __name__ == '__main__':
    oracle = RandomOracle()
    print('--- generated ---')
    [print(f'{str(i).zfill(2)} -> {oracle.hash(i)}') for i in range(0,10)]
    print('--- cached ---')
    [print(f'{str(i).zfill(2)} -> {oracle.hash(i)}') for i in range(0,10)]
