import sys
from hashlib import blake2b
from random import Random
from secrets import SystemRandom

"""
This class implements a random oracle.

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
    Apply randomly generated quadratic functions to input i, then store and
    return the resulting output truncated to the desired number of digits.
    """
    def oracle(self, i, digits=64):
        if i not in self._mapping:
            c = 0
            p = []
            while c < digits:
                x, y, z = list(self._random.choices(
                    range(0, sys.maxsize),
                    k=3))

                f = lambda a: ((x*(a+1))**2)+(y*(a+1))+z
                s = str(f(i)) 
                c += len(s)
                p.append(s)

            self._mapping[i] = int(''.join(p)[:digits])

        return self._mapping[i]


if __name__ == '__main__':
    o = RandomOracle()

    # Test with some inputs
    xs = (0, 1, 3, 7, 89, 144, 360, 2048, sys.maxsize)
    maxlen = len(str(max(xs)))

    print('Inputs -> Outputs:')
    for x in xs:
        print(f'{str(x).rjust(maxlen)} -> {o.oracle(x)}')
