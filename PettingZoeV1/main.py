import warnings

import numpy as np
from gym import spaces

from pettingzoo import AECEnv
# import playTurn as pt
from .table import Table

def env():
    env = raw_env()
    env = wrappers.CaptureStdoutWrapper(env)
    env = wrappers.TerminateIllegalWrapper(env, illegal_reward=-1)
    env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    return env

metadata = {
    "render_modes" : [],
    "name": "LiarsDice"
}


class raw_env(AECEnv):

    def __init__(self,numPlayers=4,dice=5):
        super().__init__()
        self.numPlayers = numPlayers
        self.startingDice = dice
        self._moves = ["RAISE","BS","EXACT"]

        self.possible_agents = ["player_" + str(r) for r in range(numPlayers)]
        self.agent_name_mapping = dict(zip(self.possible_agents, list(range(len(self.possible_agents)))))

        self._action_spaces = {i: spaces.Discrete((numPlayers*dice)+9) for i in self.possible_agents}
        self.observation_spaces = {i: spaces.Discrete(10) for i in self.possible_agents}

    @functools.lru_cache(maxsize=None)
    def observation_space(self,agent):
        return Discrete(4)

    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        return Discrete((self.numPlayers*self.startingDice)+9)

     def render(self, mode="human"):
        '''
        Renders the environment. In human mode, it can print to terminal, open
        up a graphical window, or open up some other display that a human can see and understand.
        '''
        if len(self.agents) == self.numPlayers:
            string = "not over yet WIP"
            # for x in range(self.numPlayers):
                # string += "".format(self.state[self.agents[x]])
            # string = ("Current state: Agent1: {} , Agent2: {}".format(MOVES[self.state[self.agents[0]]], MOVES[self.state[self.agents[1]]]))
        else:
            string = "Game over"
        print(string)


     def observe(self, agent):
        '''
        Observe should return the observation of the specified agent. This function
        should return a sane observation (though not necessarily the most up to date possible)
        at any time after reset() is called.
        '''
        # observation of one agent is the previous state of the other
        return np.array(self.observations[agent])


    def close(self):
        '''
        Close should release any graphical displays, subprocesses, network connections
        or any other environment data which should not be kept around after the
        user is no longer using the environment.
        '''
        pass

    def reset(self):
        '''
        Reset needs to initialize the following attributes
        - agents
        - rewards
        - _cumulative_rewards
        - dones
        - infos
        - agent_selection
        And must set up the environment so that render(), step(), and observe()
        can be called without issues.

        Here it sets up the state dictionary which is used by step() and the observations dictionary which is used by step() and observe()
        '''
        self.agents = self.possible_agents[:]
        self.rewards = {agent: 0 for agent in self.agents}
        self._cumulative_rewards = {agent: 0 for agent in self.agents}
        self.dones = {agent: False for agent in self.agents}
        self.infos = {agent: {} for agent in self.agents}
        self.state = {agent: NONE for agent in self.agents}
        self.observations = {agent: NONE for agent in self.agents}
        self.num_moves = 0
        '''
        Our agent_selector utility allows easy cyclic stepping through the agents list.
        '''
        self._agent_selector = agent_selector(self.agents)
        self.agent_selection = self._agent_selector.next()



    def step(self,action):
        if self.dones[self.agent_selection]:
            # handles stepping an agent which is already done
            # accepts a None action for the one agent, and moves the agent_selection to
            # the next done agent,  or if there are no more done agents, to the next live agent
            return self._was_done_step(action)

        assert (self.board.legal(action)), "played illegal move"
        agent = self.agent_selection



        # self._cumulative_rewards[agent] = 0

        # self.state[self.agent_selection] = action

        # if action["state"]
