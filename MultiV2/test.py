from __future__ import print_function
import os
import neat
import random
import visualize
# import evaluation
import pickle
VALUES = {0:"pass", 1:"Raise", 2:"BS",-1:"headCount",-2:"currentCoins",-3:"passCount",-4:"currentBet",-5:"totalCoins",-6:"playersAlive"}
def coinflip(amount):
    result = 0
    for _ in range(amount):
        if random.random() > .5:
            result += 1
    return result



def run(config_file,genome_path):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    with open(genome_path, "rb") as f:
        genome = pickle.load(f)

    # genomes = [(1, genome)]
    print(genome)


    result = {0:0,1:0,2:0}
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    currentCoins = 1
    headCount = 1
    passCount = 0
    playersAlive = 4
    for i in range(5,16+currentCoins):
        totalCoins = i
        currentBet = i-4
        currentBet = random.randint(1,totalCoins)

        output = net.activate((currentCoins,headCount,passCount,currentBet,totalCoins,playersAlive))
        end_index = output.index(max(output))


        print(f"output: {VALUES[end_index]} | currentCoins: {currentCoins} | headCount: {headCount} | passCount: {passCount} | totalCoins: {totalCoins} | currentBet: {currentBet} | playersAlive: {playersAlive}")

    visualize.draw_net(config, genome, True,node_names = VALUES)
        # headCount = coinflip(currentCoins)
        # passCount = 0
        # passCount = random.randint(0,2)



    # for i in range(10):
        # currentCoins = random.randint(1,5)
        # headCount = coinflip(currentCoins)
        #
        # passCount = random.randint(0,2)
        #
        # playersAlive = random.randint(2+passCount,4)
        #
        # totalCoins = random.randint(currentCoins+playersAlive,20-(5-currentCoins))
        # currentBet = random.randint(1,totalCoins)

        # output = net.activate((currentCoins,headCount,passCount,currentBet,totalCoins,playersAlive))
        # end_index = output.index(max(output))
        # if(end_index ==2):
        # print(f"output: {VALUES[end_index]} | currentCoins: {currentCoins} | headCount: {headCount} | passCount: {passCount} | totalCoins: {totalCoins} | currentBet: {currentBet} | playersAlive: {playersAlive}")
        # print(f" headCount: {headCount} | passCount: {passCount} | currentBet: {currentBet} | output: {VALUES[end_index]}")
        # result[end_index] += 1
    # print(result)

    # game(genomes, config)


    # p = neat.Checkpointer.restore_checkpoint("C:\\Users\\rosha\\github\\GITHUB\\MultiV1\\checkpoints\\CHK-9")
    # p.run(evaluation.eval_genomes, 10)
    # pe = neat.ParallelEvaluator(4, eval_genome)
    # winner = p.run(pe.evaluate,1)
    # print('\nBest genome:\n{!s}'.format(winner))
    # net = neat.nn.FeedForwardNetwork.create(winner, config)
    # WinnerTree = {"Raise":[0],"BS":[0],"Equal":[0]}
    # for _ in range(10000):
        # x = random.randint(5,15)
        # guess = random.randint(0,x)
        # flips = coinflip(x)
        # headCount = random.randint(0,5)
        # output = net.activate((x,guess) )
        # end_index = output.index(max(output))
        # if end_index == 0:
            # "Raise":
        #     if flips>guess:
        #         WinnerTree["Raise"][0] += 1
        #     else:
        #         WinnerTree["Raise"][1] += 1
        # elif end_index==1:
        #     if flips < guess:
        #         WinnerTree["BS"][0] += 1
        #     else:
        #         WinnerTree["BS"][1] += 1
        # else:
        #     if flips == guess:
        #         WinnerTree["Equal"][0] += 1
        #     else:
        #         WinnerTree["Equal"][1] += 1
    # print(WinnerTree)
        # print(f"x : {x} | guess : {guess} | flips : {flips} | output : {VALUES[end_index]}")



if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config')
    genome_path = os.path.join(local_dir,"results\\winner15.pkl")
    run(config_path,genome_path)
