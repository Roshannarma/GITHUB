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



class LDice:
    def __init__(self,config,runs,genomes):
        self.config = config
        self.runs = runs
        self.players = {}
        self.genomes = genomes
        self.scores = []


    def playRound(self):
        pass


    def playGame(self):
        while True:
            playRound()
            if self.roundEnd:
                


    def playGames(self):
        for genome_id,genome in self.genomes:
            players[i] = gp.player(genome,config,DICE,i)
            i += 1
        for _ in range(runs):
            resetGame()
            playGame()
        for i in range(len(self.genomes)):
            self.genomes[i][1].fitness = scoreList[i]
        return self.genomes



def eval_group(genomes,config):
    env = LDice(config,1000,genomes)
    return env.playGames()


def eval_genomes(self,genomes,config):
    genomeChunks = []
    chunk_size = 4
    for i in range(0, len(genomes), chunk_size):
        genomeChunks.append(genomes[i:i+chunk_size])
    part_group = partial(eval_group,config=config)
    pool = multiprocessing.Pool()
    genomeChunks = pool.map(part_group,genomeChunks)
    pool.close()

    WinnersBracket = []
    if len(genomeChunks)>=2:
        for genomeChunk in genomeChunks:
            winner = -1
            value = 0
            # loc = -1
            for genome_id,genome in enumerate(genomeChunk):
                # loc += 1
                if genome.fitness > value:
                    winner = loc
                    value = genome.fitness
            WinnersBracket.append(genomeChunk[winner])
        eval_genomes(WinnersBracket,config)
        for genome_id,genome in WinnersBracket:
            genome.fitness += 1000

    numGenomes = len(genomes)
    for i in range(0, numGenomes, 1):
        for x in range(0,chunk_size,1):
            if numGenomes <= (chunk_size*i)+x:
                break
            genomes[(chunk_size*i)+x][1].fitness = genomeChunks[i][x][1].fitness


    return genomes
