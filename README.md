# random-oracle

A random oracle is a 'black box' that responds to each input with an output
that is truly random. It is idempotent, so on successive calls, the output
will not change as long as the input doesn't change.

I've made a simple python class to learn about this pattern. According to Bellare and Rogaway "the random oracle produces a bit-string of
infinite length which can be truncated to the length desired". My class takes integers as inputs and outputs integers as digit strings of arbitrary length instead. One can always convert the outputs to binary, for example: `bin(int('64256680247222349271835474023544'))[2:]` results in `'1100101011000010001000100000100000101001010011111001011010000001010100001011100000100100100101010001111000'`.

The class has constructor arguments that change its source of randomness. It can use the old
`random.Random` if seeding is a requirement, `secrets.SystemRandom` when use of
`/dev/urandom` is needed or it can fetch random numbers from the [ANU QRNG](https://qrng.anu.edu.au/) quantum random number generator api. Quantum random numbers are prefetched so
there may be an initial delay when constructing the class with `use_qrn=True`.

In general it works by taking 3 random numbers, generating a quadratic function
and applying it to the input. This process is repeated until the output has the
desired amount of digits.

## General usage
```
from oracle import RandomOracle
o = RandomOracle()
foo(o.rand(42))
bar(o.rand(42, 4096))
```

### Using `secrets.SystemRandom` (default):
```
>>> o = RandomOracle()
rng source: secrets.SystemRandom
>>> o.rand(42, 32)
{'in': 42, 'out': '64256680247222349271835474023544', 'digits': 32}
>>> o.rand(42, 64)
{'in': 42, 'out': '6425668024722234927183547402354433128727958598695401521858554967', 'digits': 64}
>>> o.rand(42, 16)
{'in': 42, 'out': '6425668024722234', 'digits': 16}

```
### Using `random.Random`:
```
>>> o = RandomOracle(seed=127)
rng source: random.Random
>>> o.rand(42, 32)
{'in': 42, 'out': '31254644062366843432856949844570', 'digits': 32}
>>> o.rand(42, 64)
{'in': 42, 'out': '3125464406236684343285694984457015128614985766912090853797728353', 'digits': 64}
>>> o.rand(42, 16)
{'in': 42, 'out': '3125464406236684', 'digits': 16}
```

### Using the ANU QRNG api:
```
>>> o = RandomOracle(use_qrn=True)
rng source: ANU QRNG api
buffering 1024 quantum random numbers..
>>> o.rand(42, 32)
{'in': 42, 'out': '98402140582296609043181070266187', 'digits': 32}
>>> o.rand(42, 64)
{'in': 42, 'out': '9840214058229660904318107026618713874032176081240351014891165138', 'digits': 64}
>>> o.rand(42, 16)
{'in': 42, 'out': '9840214058229660', 'digits': 16}
```
