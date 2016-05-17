#Constant time sampling from Python dictionaries

Sampling a uniformly random item from a Python dictionary can only be done in linear time to the number of elements in the dictionary. However, the dictionaries in CPython (the default implementation of Python) are implemented as open addresing hash tables which allow for constant time sampling of uniformly random elements. The purpose of this library is to exploit this feature of the dictionary implementation and give the user access to constant time sampling of Python dictionaries.

## How does it work

Dictionaries in Python are impelemented as hash maps with open addressing. That is, each key-value pair is stored exactly once in an array that usually has slightly more slots than the number of key-value pairs. The rest of slots in the array have special elements marking empty slots or slots that used to have a key-value pair that is now deleted. In the following we will call both of this type of elements empty elements. (Note that the deleted key-value pairs cannot be simply set to empty because this might break down the probing strategy which is used when two or more hash values collide.)

The sampling strategy used here is as follows: Sample uniformly randomly an integer i between 0 and N-1, where N is the lenght of the array containing the key-value pairs and the empty elements. If the slot i in the array is a key-value pair return it, otherwise start from the beginning and repeat until such slot is found. Clearly this produces a uniform sample of the key-value pairs because each slot is sampled equally likely and each key-value pair is in the array only once.

The running time of this sampling algorithm depends on the ratio of the number of key-value pairs to the total number of slots in the array. That is if we define p=K/N, where K is the number of key-value pairs, then the probability that the algorithm finishes exactly after n iterations is p*(1-p)**(n-1) and the expected number of iterations is 1/p. Python tries to keep the p value reasonable for dicts of all sizes. If the dictionary is growing and it hits the value p=2/3 then the array is considered too full and its size is multiplied by 2 or 4. That is the value of p varies between 1/6 and 2/3. There are two notable execptions. If the dictionary is very small, for example, a new dictionary that only has a single key-value pair has p=1/8, because the minimum size of the array is 8. Other exception is a dictionary where large number of key-value pairs are deleted and not replaced by new ones.



## Benchmarks

![Benchmark plot](https://raw.githubusercontent.com/bolozna/cpython-sampling/master/benchmark.png "Benchmarks")

Here the time spent for sampling a random element from a dictionary of varying size is shown. The command 'random.choice(list(myDict))' returns a uniformly random item after iterating through all items and scales thus linearly with the number of items in the dictionary. The other two commands should work have an expected time of running which is constant.  