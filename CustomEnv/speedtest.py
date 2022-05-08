from numba import jit,cuda
import random
import timeit
import numpy as np


@jit(nopython=True)
def rollDicePrime4(amount):
    x = [0,0,0,0,0,0]
    for _ in range(amount):
        num = random.randint(0,5)
        x[num] += 1
    return x


%timeit rollDicePrime4(6)
