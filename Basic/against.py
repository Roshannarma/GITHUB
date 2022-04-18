from __future__ import print_function
import os
import neat
import random
import visualize
import time
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
                genome.fitness += 3
    return genome.fitness


def run(config_file):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    p = neat.Checkpointer.restore_checkpoint('HighLowCheckpoint-24')
    pe = neat.ParallelEvaluator(4, eval_genome)
    winner = p.run(pe.evaluate,1)
    playerscore = 0
    computerscore = 0
    skip = False
    # os.system('cls')
    while playerscore < 5 and computerscore < 5:
        time.sleep(1)
        os.system('cls')
        if(skip):
            print(f"\nActual Result:\nCoinsFlipped = {x}\nCurrent guess = {guess}\nheads = {flips}")
        x = random.randint(5,15)
        guess = random.randint(0,x//2)
        flips = coinflip(x)
        human = True
        skip  = True
        print(f"playerscore = {playerscore} | computerscore = {computerscore}")
        while True:
            if human:
                print(f"\nCurrent knowledge:\nCoinsFlipped = {x}\nCurrent guess = {guess} ")
                end_index = int(input("Choice of 0 = RAISE | 1 = BS | 2 = EQUAL:\n"))
                if end_index == 0 and guess >= x:
                    computerscore += 1
                    break
                elif end_index == 0:
                    guess+=1
                    human = not human
                elif end_index == 1:
                    if flips<guess:
                        playerscore+=1
                        break
                    else:
                        computerscore+=1
                        break
                else:
                    if flips == guess:
                        playerscore += 1
                        break
                    else:
                        computerscore += 1
                        break
            else:
                net = neat.nn.FeedForwardNetwork.create(winner, config)
                output = net.activate((x,guess) )
                end_index = output.index(max(output))
                if end_index == 0 and guess >= x:
                    playerscore += 1
                    break
                elif end_index == 0:
                    print("computer raises")
                    guess+=1
                    human = not human
                elif end_index == 1:
                    print("computer calls bs")
                    if flips<guess:
                        computerscore+=1
                        break
                    else:
                        playerscore+=1
                        break
                else:
                    print("computer calls equal")
                    if flips == guess:
                        computerscore += 1
                        break
                    else:
                        playerscore += 1
                        break




if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config')
    run(config_path)
