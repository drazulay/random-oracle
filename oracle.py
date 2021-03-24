import sys
import requests
from random import Random
from secrets import SystemRandom

"""
This class implements a random oracle.

See: https://en.wikipedia.org/wiki/Random_oracle
"""
class RandomOracle(object):

    QRNG_API_URL = 'https://qrng.anu.edu.au/API/jsonI.php'

    def __init__(self, seed=None, use_qrng=True):
        # Random() can be seeded for reproducability but should not be used in
        # real world applications.
        self._random = SystemRandom() if seed is None else Random(seed)

        # Storage for oracles
        self._mapping = {}

        # Use numbers from the ANU QRNG Api for true randomness
        self._use_qrng = use_qrng


    """
    Use the ANU QRNG api to fetch an array of quantum random numbers.
    See: https://qrng.anu.edu.au/
    """
    def _qrn(self, length=3, dtype='hex16', size=32):
        data = requests.get(self.QRNG_API_URL,
                {'length': length, 'type': dtype, 'size': size}).json()
        
        return [int(x, 16) for x in data['data']]



    """
    Apply randomly generated quadratic functions to input i, then store and
    return the resulting output truncated to the desired number of digits.
    """
    def oracle(self, i, digits=64):
        old_p = self._mapping.get(i, '')
        f = lambda a: ((x*(a+1))**2)+(y*(a+1))+z

        if i not in self._mapping or len(old_p) < digits:
            c = len(old_p)
            p = [old_p]
            while c < digits:
                x, y, z = list(self._qrn()) if self._use_qrng else list(
                        self._random.choices(range(0, sys.maxsize), k=3))

                s = str(f(i)) 
                c += len(s)
                p.append(s)

            self._mapping[i] = ''.join(p)

        return int(self._mapping[i][:digits])


if __name__ == '__main__':
    o = RandomOracle(use_qrng=True)

    # Test with some inputs
    xs = (0, 1, 3, 7, 89, 144, 360, 2048, sys.maxsize)
    maxlen = len(str(max(xs)))

    print('Inputs -> Outputs:')
    for x in xs:
        print(f'{str(x).rjust(maxlen)} -> {o.oracle(x)}')
