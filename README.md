# random-oracle

A random oracle is a 'black box' that responds to each input with an output
that is truly random. It is idempotent, so the output will not change when the
input doesn't change.

According to Bellare and Rogaway "the random oracle produces a bit-string of
infinite length which can be truncated to the length desired".

I've made a simple python class to learn about this pattern. It can use the old
`random.Random` if seeding is a requirement, `secrets.SystemRandom` when use of
`/dev/urandom` is needed or it can fetch random numbers from the ANU QRNG
quantum random number generator api. The ANU QRNG will cause slower generation
due to the api call.

In general it works by taking 3 random numbers, generating a quadratic function
and applying it to the input. This process is repeated until the output has the
desired amount of digits.

### Using `secrets.SystemRandom` (default):
```
>>> from oracle import RandomOracle
>>> o = RandomOracle()
rng source: secrets.SystemRandom
>>> o.oracle(42, digits=32)
14528330955310958865159801373664
>>> o.oracle(42, digits=64)
1452833095531095886515980137366470662963210727055033068395198181
>>> o.oracle(42, digits=16)
1452833095531095

```
### Using `random.Random`:
```
>>> from oracle import RandomOracle
>>> o = RandomOracle(seed=127)
rng source: random.Random
>>> o.oracle(42, digits=32)
31254644062366843432856949844570
>>> o.oracle(42, digits=64)
3125464406236684343285694984457045626881512861498576691209085379
>>> o.oracle(42, digits=16)
3125464406236684
```

### Using the ANU QRNG api:
```
>>> from oracle import RandomOracle
>>> o = RandomOracle(use_qrn=True)
rng source: ANU QRNG api
buffering 1024 quantum random numbers..
done
>>> o.oracle(42, digits=32)
16616476605623646468935274835361
>>> o.oracle(42, digits=64)
1661647660562364646893527483536191620530671230464389866141863745
>>> o.oracle(42, digits=16)
1661647660562364
```
