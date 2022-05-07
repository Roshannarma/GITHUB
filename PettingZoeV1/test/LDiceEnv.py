from pettingzoo import AECEnv
from pettingzoo.utils import wrappers
from pettingzoo.utils import agent_selector
import functools
from gym import Discrete

BET_NUMBER = 14

def combine(rolls):
    combination = [0]*6
    for index in range(6):
        for key in rolls:
            combination[index] += rolls[key][index]
    return combination

# def combine(rolls):
    # return list(map(,rolls.values()))




# import jax.numpy as jnp
# import timeit
#
#
# def testFunc(x):
#     return jnp.sum(x)
#
# x = jnp.array([10]*1000)
# testFunc(x)

from numba import jit,cuda
import random
import timeit
import numpy as np
@jit(nopython=True)
def go_fast(a): # Function is compiled to machine code when called the first time
    trace = 0.0
    # assuming square input matrix
    for i in range(a.shape[0]):   # Numba likes loops
        trace += np.tanh(a[i, i]) # Numba likes NumPy functions
    return a + trace

x = np.arange(100).reshape(10, 10)
go_fast(x)

go_fast(2*x)

%timeit go_fast(x)

%timeit go_fast.py_func(x)


# @cuda.jit
# def increment_by_one(an_array):
#     # Thread id in a 1D block
#     tx = cuda.threadIdx.x
#     # Block id in a 1D grid
#     ty = cuda.blockIdx.x
#     # Block width, i.e. number of threads per block
#     bw = cuda.blockDim.x
#     # Compute flattened index inside the array
#     pos = tx + ty * bw
#     if pos < an_array.size:  # Check array boundaries
#         an_array[pos] += 1

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
increment_by_one[blockspergrid, threadsperblock](an_array)

%timeit increment_by_one[blockspergrid, threadsperblock](an_array)

an_array = np.array([0]*100000)

%timeit increment_by_one_py(an_array)


rolls = {
    "player_1": [0,1,0,4,0,0],
    "player_2": [0,1,0,4,0,0],
    "player_3": [2,0,2,0,0,1],
    "player_4": [0,1,0,4,0,0],
}
combine(rolls)

def env(*kwargs):
    env = wrappers.OrderEnforcingWrapper(env)
    env = raw_env(*kwargs)
    return env

class raw_env(AECEnv):
    def __init__(self,numPlayers=4):
        self.agents = ["player_" + str(r) for r in range(numPlayers)]


        self.action_spaces = {i:Discrete(5) for i in self.agents}
        self.observation_spaces = {i:Discrete(15) for i in self.agents}
        self.rolls = {i:roll(5) for i in self.agents}
        self.info = {
            "betPlayer": -1,
            "dice": combine(self.rolls)
        }
        # self.alive = {i:True for i in self.agents}


    def render(self, mode="human"):
        # Ignore render until finished
        pass

    def observe(self, agent):
        pass
        # self.observation_spaces[agent]

    def close(self):
        pass

    def reset(self):
        pass

    def newRound(self):
        pass

    def roundEnd(self,agent,win):
        if win:
            self.rewards[agent] = 1
        else:
            self.rewards[agent] = -1
        self.dones = {i: True for i in self.agents}
        # self.rewards[]
        # pass

    def step(self, action = -1, pip = -1, amount = -1):
        # main priority steps include
        # update rewards
        # update cumulative_rewards
        # dones
        # infos
        # move to next agent
        # if roundend:
            # newRound()

        assert (action != -1), "did not input action"
        assert (pip != -1 ), "did not input pip"
        assert (amount != -1), "did not input amount"

        assert (pip in range(7)), "pip value out of bounds"
        # assert (amount in range(20)), "amount value out of bounds"

        assert (action in range(3)), "action out of bounds"

        agent = self.agent_selection

        # if not self.alive(agent):
        #     return

        if not amount in range(20):
            self.roundEnd(agent,win=False)

        # if currentbet player doesn't exist, it must raise
        # if current betplayer is itself, win round

        # complete action

        # RAISE
        if action == 0:
            # assert (pip in range(7)), "pip value out of bounds"
            # assert (amount in range(20)), "amount value out of bounds"
            if amount < self.observation_space(agent)[BET_NUMBER] or (amount == self.observation_space(agent)[BET_NUMBER] and pip <= self.observation_space["betPip"]):
                self.roundEnd(agent, win=False)
            updateObservationSpaces()
            pass

        # BS
        elif action == 1:
            if self.observation_space(agent)[BET_NUMBER] > self.info["dice"][pip-1]:
                self.roundEnd(self.info["betPlayer"], win=False)
            else:
                self.roundEnd(agent, win=False)
            pass

        # Exact
        else:
            if self.observation_space(agent)[BET_NUMBER] == self.info["dice"][pip-1]:
                self.roundEnd(agent,win=True)
            else:
                self.roundEnd(self.info["betPlayer"],win=False)



        # updateObservationSpaces()


        # if roundEnded resetRound with changed values(likely call function)

        if
        self._accumlate_rewards()

    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        return self.observation_spaces[agent]

    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        return self.action_spaces[agent]
