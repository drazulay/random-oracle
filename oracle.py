from hashlib import blake2b
from secrets import token_bytes

"""
See: https://en.wikipedia.org/wiki/Random_oracle
"""
class RandomOracle(object):

    def __init__(self, digest_size=32):
        self.digest_size = digest_size
        self.mapping = {}

    def hash(self, i):
        if i not in self.mapping:
            self.mapping[i] = blake2b(token_bytes(64),
                    salt=token_bytes(16),
                    person=token_bytes(16),
                    key=token_bytes(64),
                    digest_size=self.digest_size).hexdigest()

        return self.mapping[i]

if __name__ == '__main__':
    oracle = RandomOracle()
    print('--- round 1 ---')
    [print(f'{str(i).zfill(2)} -> {oracle.hash(i)}') for i in range(0,10)]
    print('--- round 2 ---')
    [print(f'{str(i).zfill(2)} -> {oracle.hash(i)}') for i in range(0,10)]
