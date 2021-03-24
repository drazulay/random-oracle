# random-oracle

A random oracle is a 'black box' that responds to each input with an output
that is truly random. It is idempotent, so the output will not change when the
input doesn't change.

According to Bellare and Rogaway "the random oracle produces a bit-string of
infinite length which can be truncated to the length desired".

```
>>> from oracle import RandomOracle
>>> o = RandomOracle()
>>> o.oracle(32)
1050635442812937345375111631043694528819210620053500242169675007
>>> o.oracle(32)
1050635442812937345375111631043694528819210620053500242169675007
>>> o.oracle(31)
1100916330618339260426614831690309520384761187699683367438936379
>>> o.oracle(31)
1100916330618339260426614831690309520384761187699683367438936379
>>> o.oracle(28)
1033761021502373269839283522969242525696024369714198946127107354
>>> o.oracle(28)
1033761021502373269839283522969242525696024369714198946127107354
```

# Todo
- Add new digits when oracle is called again with the same input but a higher number of digits.
