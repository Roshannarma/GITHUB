from pettingzoo import AECEnv
from pettingzoo.utils import wrappers
from pettingzoo.utils import agent_selector
import functools

env(first="text",second=2)
args = ["text",2]
kwargs = {"first":"text","second":2}

greet_me("hello","text")

# test_var_args("hello","text")
# def greet_me(kwargs):
    # for key, value in kwargs.items():
        # print("{0} = {1}".format(key, value))

def test_var_args(*args):
    test_var_args2(*args)
    # for arg in argv:
        # print("another arg through *argv:", arg)

def test_var_args2(*args):
    # print("first normal arg:", f_arg)
    for arg in args:
        print("another arg through *argv:", arg)

def env(*args):
    env = wrappers.OrderEnforcingWrapper(env)
    env = raw_env(*args)
    return env

class raw_env(AECEnv):
    def __init__(self,numPlayers=4):
        self.possible_agents = ["player_" + str(r) for r in range(numPlayers)]


    def render(self, mode="human"):
        pass

    def observe(self, agent):
        pass

    def close(self):
        pass

    def reset(self):
        pass

    def step(self, action):
        pass

    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        pass

    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        pass
