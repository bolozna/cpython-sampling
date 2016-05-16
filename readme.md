#Linear time sampling from Python data structures

Sampling a uniformly random item from a Python dictionary can only be done in linear time to the number of elements in the dictionary. However, the dictionaries in CPython (the default implementation of Python) are implemented as hash tables which allow for constant time sampling of uniformly random elements. The purpose of this library is to exploit this feature of the dictionary implementation and give the user access to constant time sampling of Python dictionaries.

## Benchmarks

![Benchmark plot](https://raw.githubusercontent.com/bolozna/cpython-sampling/master/benchmark.png "Benchmarks")

Here the time spent for sampling a random element from a dictionary of varying size is shown. The command 'random.choice(list(myDict))' returns a uniformly random item after iterating through all items and scales thus linearly with the number of items in the dictionary. The other two commands should work have an expected time of running which is constant.  