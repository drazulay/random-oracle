import sys
import requests
import numpy as np

from random import Random
from secrets import SystemRandom

"""
This class implements a random oracle.

See: https://en.wikipedia.org/wiki/Random_oracle
"""
class RandomOracle(object):

    QRNG_API_URL = 'https://qrng.anu.edu.au/API/jsonI.php'

    def __init__(self, seed=None, use_qrn=False, qrn_n_preload=1024):
        # Random() can be seeded for reproducability but should not be used in
        # real world applications.
        self._random = SystemRandom() if seed is None else Random(seed)

        # Storage for oracles
        self._mapping = {}

        # ANU QRNG api
        self._qrn_data = []
        self._qrn_n_preload = qrn_n_preload
        self._use_qrn = use_qrn

        if use_qrn:
            print('rng source: ANU QRNG api')
            self._qrn_preload()
        elif seed is None:
            print('rng source: secrets.SystemRandom')
        else:
            print('rng source: random.Random')


    """
    Use the ANU QRNG api to fetch an array of quantum random numbers.
    See: https://qrng.anu.edu.au/
    """
    def _qrn_preload(self):
        print(f'buffering {self._qrn_n_preload} quantum random numbers..')
        try:
            data = requests.get(self.QRNG_API_URL, {
                'length': self._qrn_n_preload,
                'type': 'hex16',
                'size': 32}).json()

            self._qrn_data = data['data']
        except:
            print('Error fetching data from ANU QRNG api')
            exit(1)


    """
    Return n quantum random numbers
    """
    def _qrn(self, n=3):
        # If there's a buffer underflow preload some numbers from the api
        if len(self._qrn_data) < n:
            self._qrn_preload()

        return [int(self._qrn_data.pop(), 16) for x in range(n)]


    """
    Apply a quadratic function with random parameters to input i
    """
    def _qf(self, i):
        x, y, z = list(self._qrn()) if self._use_qrn else list(
                self._random.choices(range(0, sys.maxsize), k=3))

        return ((x*(i+1))**2)+(y*(i+1))+z


    """
    Generate an oracle for input i, store it and truncate the output to the
    desired number of digits.
    """
    def rand(self, i, digits=64):
        data = self._mapping.get(i, {})
        p = [data.get('out', '')]
        c = len(p)

        while c < digits:
            s = str(self._qf(i)) 
            c += len(s)
            p.append(s)

        o = ''.join(p)

        self._mapping[i] = {
            "in": i,
            "out": o[:digits],
            "digits": digits}

        return self._mapping[i]


if __name__ == '__main__':
    o = RandomOracle(seed=1)
    [print(f'{o.rand(x)}') for x in (0, 1, 0, 2, 1, 2, sys.maxsize)]

    o = RandomOracle()
    [print(f'{o.rand(x)}') for x in (0, 1, 0, 2, 1, 2, sys.maxsize)]

    o = RandomOracle(use_qrn=True)
    [print(f'{o.rand(x)}') for x in (0, 1, 0, 2, 1, 2, sys.maxsize)]
        
