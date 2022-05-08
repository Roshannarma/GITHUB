from neat.graphs import feed_forward_layers
from neat.six_util import itervalues

import numba
from numba import jit, njit
from numba.typed import List, Dict
import numpy as np
import math
import os
import neat
import random
import time
LOCALDIR = os.path.dirname(__file__)

SAMPLE = numba.typed.List([
20, #totalDice
0,
1,
0,
0,
0,
5, #owner dice
4, #playersAlive
0,
0,
1,
0,
0,
0, #betPip
5
])

# @jit(nopython=True)
# def activate(input_nodes, output_nodes, node_evals_node, node_evals_bias, node_evals_resp, node_evals_ins_nodes, node_evals_ins_conns, values, inputs):
#     for i in range(input_nodes.size):
#         values[input_nodes[i]] = inputs[i]
#
#     for node in range(len(node_evals_node)):
#         s = 0
#         for pred in range(len(node_evals_ins_nodes[node])):
#             s += values[node_evals_ins_nodes[node][pred]] * node_evals_ins_conns[node][pred]
#
#         values[node_evals_node[node]] = math.tanh(node_evals_bias[node] + node_evals_resp[node] * s)
#
#     return [values[output_nodes[i]] for i in range(output_nodes.size)]

# @jit()
# def activate(self, inputs):
#     if len(self.input_nodes) != len(inputs):
#         raise RuntimeError("Expected {0:n} inputs, got {1:n}".format(len(self.input_nodes), len(inputs)))
#
#     for k, v in zip(self.input_nodes, inputs):
#         self.values[k] = v
#
#     for node, act_func, agg_func, bias, response, links in self.node_evals:
#         node_inputs = []
#         for i, w in links:
#             node_inputs.append(self.values[i] * w)
#         s = agg_func(node_inputs)
#         self.values[node] = act_func(bias + response * s)
#
#     return [self.values[i] for i in self.output_nodes]

# @jit(nopython=True)
def activate(neuralDict, floatList,Link1List,Link2List,inputs):
    # print(len(neuralDict[0]))
    values = neuralDict[1]
    # print(len(Link1List[0]))
    # print(len(values))
    # print(len(neuralDict[0]))
    # print(len(Link1List[0]))
    if len(neuralDict[0]) != len(inputs):
        raise RuntimeError("fuck me")
    for k, v in zip(neuralDict[0], inputs):
        values[k] = v
    # print(len(values))
    for i in range(len(neuralDict[0])):
        # print(i)
        node = neuralDict[0][i]
        node_inputs = List()
        # try:
        for j in range(len(Link1List)):
            node_inputs.append(Link1List[j][i] * Link2List[j][i])
        # s = sum(node_inputs)
        # print(node_inputs)
    # print(" ")
        # except:
        #     print(i)
        #     print(Link1List)
        #     print("this broke")
        #     raise RuntimeError("broken")
    #         print((Link1List[i][j]*-1)-1)
    #         print(Link2List[i])
    #         print(Link2List[i][j])
    #         print(" ")
    #         node_inputs.append( values[(Link1List[i][j]*-1)-1] * Link2List[i][j] )
    #         print("2nd")
    #     print("1st")
    # print("here")

        # bias =

    # for node, act_func, agg_func, bias, response, links in node_evals:
    #     node_inputs = []
    #     for i, w in links:
    #         node_inputs.append(values[i] * w)
    #     s = agg_func(node_inputs)
    #     values[node] = act_func(bias + response * s)
    # print()
    # pass

    # return [neuralDict["values"][i] for i in neuralDict["output_nodes"]]



class FeedForwardNetwork(object):
    def __init__(self, inputs, outputs, node_evals):
        self.input_nodes = inputs
        self.output_nodes = outputs
        self.node_evals = node_evals
        self.values = dict((key, 0.0) for key in inputs + outputs)


    def activate(self, inputs):
        if len(self.input_nodes) != len(inputs):
            raise RuntimeError("Expected {0:n} inputs, got {1:n}".format(len(self.input_nodes), len(inputs)))

        for k, v in zip(self.input_nodes, inputs):
            self.values[k] = v

        for node, act_func, agg_func, bias, response, links in self.node_evals:
            node_inputs = []
            for i, w in links:
                node_inputs.append(self.values[i] * w)
            s = agg_func(node_inputs)
            self.values[node] = act_func(bias + response * s)

        return [self.values[i] for i in self.output_nodes]

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





# def eval_single_genome(genome, config, thread_id, result):
#     net = neat.nn.FeedForwardNetwork.create(genome, config)
#
#     error_sum = 0
#
#     for i, row in PRICES.iterrows():
#         prediction = feed_forward.activate(net.input_nodes, net.output_nodes, net.node_evals_node, net.node_evals_bias, net.node_evals_resp, net.node_evals_ins_nodes, net.node_evals_ins_conns, net.values, np.array([0]))
#         error_sum += (prediction - PRICES.iloc[i]['open']) ** 2

    # result[thread_id] = error_sum


@jit
def combine(x):
    sum = 0
    for num in x:
        sum += num
    return sum


def eval_genomes(genomes, config):
    # x = True
    total = 0
    for genome_id, genome in genomes:
        # x = time.time()
        net = FeedForwardNetwork.create(genome, config)
        # total += time.time()-x
        # print(time.time()-x)
        # neuralDict = {
        #     "input_nodes": net.input_nodes,
        #     "values" : net.values,
        #     "node_evals":net.node_evals,
        #     "output_nodes":net.output_nodes
        # }
        # print(net.node_evals[0])
        # if x:
        x = time.time()
        NodeList = List()
        BiasList = List()
        ResponseList = List()
        Link1List = List()
        Link2List = List()
        # total += time.time()-x
        for node, act_func, agg_func, bias, response, links in net.node_evals:
            NodeList.append(node)
            BiasList.append(bias)
            ResponseList.append(response)
            list1,list2 = zip(*links)
            Link1List.append(List(list1))
            Link2List.append(List(list2))
            # print(links)
            # print(list1)
            # print(list2)
        total += time.time()-x

# have to hardcode agg_func and act_func
        neuralDict = List([
            List(net.input_nodes),
            List(net.values),
            NodeList,
        ])

        floatList = List([
        ResponseList,
        BiasList,
        ])

        error_sum = 0
        # total += time.time()-x
        # print(Link2List)
        # print()
        for _ in range(10):
            prediction = activate(neuralDict, floatList,Link1List,Link2List,SAMPLE)


        # for _ in range(1000):
        #     prediction = activate(neuralDict, floatList,Link1List,Link2List,SAMPLE)

        genome.fitness = random.randint(1,100)
    print(total)
    return genomes


def run(config_file):

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    p = neat.Population(config)

    ITERATIONS = int(input("What number of iterations do you want?:\n"))

    x = time.time()
    winner = p.run(eval_genomes, ITERATIONS)
    print(time.time()-x)
    # print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    # local_dir = os.path.dirname(__file__)
    config_path = os.path.join(LOCALDIR, 'config')
    run(config_path)
