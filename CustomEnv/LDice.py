from numba import jit,cuda
import random
import timeit
import numpy as np
import neat

SAMPLE = [
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
]
# SAMPLE


@jit()
def activation(net,inputs):
    return net.activate(inputs)

class LDice:
    def __init__(self,config,chunk_size = 4):
        self.chunk_size = chunk_size
        self.genomeChunks = []
        # self.pool = multiprocessing.Pool()
        self.config = config



    def eval_genomes(self,genomes,config):
        for genome_id,genome in genomes:
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            for _ in range(10000):

                net.activate(SAMPLE)
            genome.fitness = random.randint(1,100)
        return genomes

    # def eval_genomes2(self,genomes,config):
    #     for genome_id,genome in genomes:
    #         net = neat.nn.FeedForwardNetwork.create(genome, config)
    #         for _ in range(10000):
    #             activation(net,SAMPLE)
    #             # net.activate(SAMPLE)
    #         genome.fitness = random.randint(1,100)
    #     return genomes

    # def eval_genomes_pool(self,genomes,config):
    #     for genome_id,genome in genomes:
    #         net = neat.nn.FeedForwardNetwork.create(genome, config)
    #         for _ in range(10000):
    #             net.activate(SAMPLE)
    #         genome.fitness = random.randint(1,100)
    #     return genomes


# temp = LDice(1)

# temp.eval_genomes(1,1)
