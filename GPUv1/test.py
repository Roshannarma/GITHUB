from numba import jit,cuda
import random
import timeit
import numpy as np




@jit
def increment_by_one_jit(an_array):
    for i in range(len(an_array)):
        an_array[i] += 1

@cuda.jit
def increment_by_one(an_array):
    pos = cuda.grid(1)
    if pos < an_array.size:
        an_array[pos] += 1

def increment_by_one_py(an_array):
    for i in range(len(an_array)):
        an_array[i] += 1



an_array = np.array([0]*100000)
threadsperblock = 32
blockspergrid = (an_array.size + (threadsperblock - 1)) // threadsperblock
# increment_by_one[blockspergrid, threadsperblock](an_array)

# %timeit increment_by_one[blockspergrid, threadsperblock](an_array)

x_an_array = cuda.to_device(an_array)

t = timeit.timeit(lambda: increment_by_one[blockspergrid, threadsperblock](x_an_array),number=1000)
print(t)
x_an_array.dtype
an_array
timeit.timeit(lambda:x_an_array.copy_to_host(),number=1)

t = timeit.timeit(lambda: increment_by_one_py(an_array),number=100)
print(t)

t = timeit.timeit(lambda: increment_by_one_jit(an_array),number=1000)
print(t)
# an_array = np.array([0]*100000)
# threadsperblock = 64
# blockspergrid = (an_array.size + (threadsperblock - 1)) // threadsperblock
# increment_by_one[blockspergrid, threadsperblock](an_array)

# %timeit increment_by_one[blockspergrid, threadsperblock](an_array)
