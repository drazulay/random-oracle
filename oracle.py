import sys
from hashlib import blake2b
from random import Random
from secrets import SystemRandom, token_bytes

"""
See: https://en.wikipedia.org/wiki/Random_oracle
"""
class RandomOracle(object):

    def __init__(self, seed=None):
        # Random() can be seeded for reproducability but should not be used in
        # real world applications.
        self._random = SystemRandom() if seed is None else Random(seed)

        # Storage for oracles
        self._mapping = {}


    """
    Stores and returns the truncated output of a randomly generated quadratic
    function applied to input i.

    All numbers generated are at least 32 digits long, but thereafter it can be
    deduced from the number of digits of the output how large the input was.

    TODO:
    According to Bellare and Rogaway "the random oracle produces a bit-string
    of infinite length which can be truncated to the length desired" so I think
    I need to implement this some other way, perhaps using a generator and
    the fibonacci sequence in some way.
    """
    def oracle(self, i):
        if i not in self._mapping:
            # Pick 3 potentially large random integers
            x, y, z = list(self._random.choices(range(0, sys.maxsize), k=3))
            # Use them to construct a quadratic function
            f = lambda a: ((x*(a+1))**2)+(y*(a+1))+z
            # Apply it to i, cut off after 32 digits and store the output
            self._mapping[i] = int(str(f(i))[:32])

        return self._mapping[i]


    def hash(self, i, hashfunc=blake2b, **hashfunc_params):
        oracle = self.oracle(i).to_bytes(
                sys.int_info.bits_per_digit * sys.int_info.sizeof_digit,
                byteorder='big')

        return hashfunc(oracle, **hashfunc_params)

if __name__ == '__main__':
    o = RandomOracle()
    # Test with some inputs
    xs = (0, 1, 3, 7, 89, 144, 360, 2048, sys.maxsize)
    maxlen = len(str(max(xs)))

    print('Inputs -> Outputs:')
    for x in xs:
        print(f'{str(x).rjust(maxlen)} -> {o.oracle(x)}')
