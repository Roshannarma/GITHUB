from neat.graphs import feed_forward_layers
from neat.six_util import itervalues
import neat
import numba
from numba import jit, njit,cuda
from numba.typed import List, Dict
import numpy as np
import math
import os
import random
import time
# from pyculib import rand as curand
from numba.cuda.random import create_xoroshiro128p_states, xoroshiro128p_uniform_float32

LOCALDIR = os.path.dirname(__file__)


@njit()
def activate(self, inputs):
    pass
    # if len(self.input_nodes) != len(inputs):
    #     raise RuntimeError("Expected {0:n} inputs, got {1:n}".format(len(self.input_nodes), len(inputs)))
    #
    # for k, v in zip(self.input_nodes, inputs):
    #     self.values[k] = v
    #
    # for node, act_func, agg_func, bias, response, links in self.node_evals:
    #     node_inputs = []
    #     for i, w in links:
    #         node_inputs.append(self.values[i] * w)
    #     s = agg_func(node_inputs)
    #     self.values[node] = act_func(bias + response * s)
    #
    # return [self.values[i] for i in self.output_nodes]

class FeedForwardNetwork(object):
    def __init__(self, inputs, outputs, node_evals):
        self.input_nodes = inputs
        self.output_nodes = outputs
        self.node_evals = node_evals
        self.values = dict((key, 0.0) for key in inputs + outputs)


    @staticmethod
    def create(genome, config):
        """ Receives a genome and returns its phenotype (a FeedForwardNetwork). """

        # Gather expressed connections.
        connections = [cg.key for cg in genome.connections.values() if cg.enabled]

        layers = feed_forward_layers(config.genome_config.input_keys, config.genome_config.output_keys, connections)
        node_evals = []
        for layer in layers:
            for node in layer:
                inputs = []
                node_expr = [] # currently unused
                for conn_key in connections:
                    inode, onode = conn_key
                    if onode == node:
                        cg = genome.connections[conn_key]
                        inputs.append((inode, cg.weight))
                        node_expr.append("v[{}] * {:.7e}".format(inode, cg.weight))

                ng = genome.nodes[node]
                aggregation_function = config.genome_config.aggregation_function_defs.get(ng.aggregation)
                activation_function = config.genome_config.activation_defs.get(ng.activation)
                node_evals.append((node, activation_function, aggregation_function, ng.bias, ng.response, inputs))

        return FeedForwardNetwork(config.genome_config.input_keys, config.genome_config.output_keys, node_evals)

# @cuda.jit
# def eval_single_genome(genome, config, thread_id, result):
    # net = neat.nn.FeedForwardNetwork.create(genome, config)

    # error_sum = 0

    # for i, row in PRICES.iterrows():
        # prediction = feed_forward.activate(net.input_nodes, net.output_nodes, net.node_evals_node, net.node_evals_bias, net.node_evals_resp, net.node_evals_ins_nodes, net.node_evals_ins_conns, net.values, np.array([0]))
        # error_sum += (prediction - PRICES.iloc[i]['open']) ** 2
    # error_sum = random.randint(0,5)
    # result[thread_id] = error_sum


# @cuda.jit
@njit
def getRandom(rng_states, pos):
    return xoroshiro128p_uniform_float32(rng_states, pos)


@cuda.jit
def increment_by_one(rng_states, iterations, an_array):
    pos = cuda.grid(1)
    if (pos%4!=0): return
    if pos < an_array.size:
        an_array[pos] = getRandom(rng_states,pos)
        an_array[pos+1] = getRandom(rng_states,pos)
        an_array[pos+2] = getRandom(rng_states,pos)
        an_array[pos+3] = getRandom(rng_states,pos)


def eval_genomes(genomes,config):
    an_array = np.zeros(len(genomes))
    threadsperblock = 32
    blockspergrid = (an_array.size + (threadsperblock - 1)) // threadsperblock
    rng_states = create_xoroshiro128p_states(threadsperblock * blockspergrid, seed=1)
    x = time.time()
    # an_array = cuda.to_device(an_array)
    increment_by_one[blockspergrid, threadsperblock](rng_states,100,an_array)
    # an_array = an_array.copy_to_host()
    print(time.time()-x)
    for i in range(len(genomes)):
        genomes[i][1].fitness = an_array[i]
    return genomes


def run(config_file):
    config = neat.Config(neat.DefaultGenome , neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)



    p = neat.Population(config)
    ITERATIONS = int(input("What number of iterations do you want?:\n"))

    winner = p.run(eval_genomes, ITERATIONS)

    print('\nBest genome:\n{!s}'.format(winner))




if __name__ == "__main__":
    config_path = os.path.join(LOCALDIR, 'config')
    run(config_path)
