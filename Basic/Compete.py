from __future__ import print_function
import os
import neat
import random
import visualize
VALUES = {0:"Raise", 1:"BS", 2:"Equal"}
def coinflip(amount):
    result = 0
    for _ in range(amount):
        if random.random() > .5:
            result += 1
    return result

def eval_genome(genome,config):
    genome.fitness = 0
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    for i in range(1000):
        x = random.randint(5,15)
        guess = random.randint(x-5,x)
        flips = coinflip(x)
        output = net.activate((x,guess))
        end_index = output.index(max(output))
        if end_index == 0:
            if flips>guess:
                genome.fitness += 1
            # this will be calling good
        elif end_index==1:
            if flips < guess:
                genome.fitness += 1
        else:
            if flips == guess:
                genome.fitness += 1
    return genome.fitness



def run(config_file):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    p = neat.Checkpointer.restore_checkpoint('HighLowCheckpoint-4')
    pe = neat.ParallelEvaluator(4, eval_genome)
    winner = p.run(pe.evaluate,1)
    print('\nBest genome:\n{!s}'.format(winner))
    net = neat.nn.FeedForwardNetwork.create(winner, config)
    WinnerTree = {"Raise":[0,0],"BS":[0,0],"Equal":[0,0]}
    for _ in range(10000):
        x = random.randint(5,15)
        guess = random.randint(0,x)
        flips = coinflip(x)
        output = net.activate((x,guess) )
        end_index = output.index(max(output))
        if end_index == 0:
            if flips>guess:
                WinnerTree["Raise"][0] += 1
            else:
                WinnerTree["Raise"][1] += 1
        elif end_index==1:
            if flips < guess:
                WinnerTree["BS"][0] += 1
            else:
                WinnerTree["BS"][1] += 1
        else:
            if flips == guess:
                WinnerTree["Equal"][0] += 1
            else:
                WinnerTree["Equal"][1] += 1
    print(WinnerTree)
        # print(f"x : {x} | guess : {guess} | flips : {flips} | output : {VALUES[end_index]}")



if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config')
    run(config_path)
