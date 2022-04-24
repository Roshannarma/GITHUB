from __future__ import print_function
import os
import neat
import random
import visualize
# import evaluation
import pickle
LOCALDIR = os.path.dirname(__file__)


VALUES = {
    -1: "total",
    -2: "# of 1's",
    -3: "# of 2's",
    -4: "# of 3's",
    -5: "# of 4's",
    -6: "# of 5's",
    -7: "# of 6's",
    -8: "# of players left",
    -9: "is1",
    -10: "is2",
    -11: "is3",
    -12: "is4",
    -13: "is5",
    -14: "is6",
    -15: "bet number",

    0: "raise",
    1: "bs",
    2: "exact",
    3: "is1",
    4: "is2",
    5: "is3",
    6: "is4",
    7: "is5",
    8: "is6",
    9: "# of dice"
}
# VALUES = {0:"exact", 1:"Raise", 2:"BS",-1:"headCount",-2:"currentCoins",-3:"currentBet",-4:"totalCoins",-5:"playersAlive"}
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

    print(genome)


    result = {0:0,1:0,2:0}
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    # currentCoins = 1
    # headCount = 1
    # passCount = 0
    # playersAlive = 4
    # for i in range(5,16+currentCoins):
        # totalCoins = i
        # currentBet = i-4
        # currentBet = random.randint(1,totalCoins)

        # output = net.activate((currentCoins,headCount,currentBet,totalCoins,playersAlive))
        # end_index = output.index(max(output))


        # print(f"output: {VALUES[end_index]} | currentCoins: {currentCoins} | headCount: {headCount} | totalCoins: {totalCoins} | currentBet: {currentBet} | playersAlive: {playersAlive}")

    visualize.draw_net(config, genome, True,node_names = VALUES)
        # headCount = coinflip(currentCoins)
        # passCount = 0
        # passCount = random.randint(0,2)



    # for i in range(100):
    #     currentCoins = random.randint(1,5)
    #     headCount = coinflip(currentCoins)
    #     #
    #     # passCount = random.randint(0,2)
    #     #
    #     playersAlive = random.randint(2,4)
    #     #
    #     totalCoins = random.randint(currentCoins+playersAlive,20-(5-currentCoins))
    #     currentBet = random.randint(1,totalCoins)
    #
    #     output = net.activate((currentCoins,headCount,currentBet,totalCoins,playersAlive))
    #     end_index = output.index(max(output))
    #     # if(end_index ==2):
    #     print(f"output: {VALUES[end_index]} | currentCoins: {currentCoins} | headCount: {headCount} | totalCoins: {totalCoins} | currentBet: {currentBet} | playersAlive: {playersAlive}")

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
    config_path = os.path.join(LOCALDIR, 'config')
    ITERATIONS = int(input("What number of iterations do you want?:\n"))
    genome_path = os.path.join(LOCALDIR,f"results\\winner{ITERATIONS}.pkl")
    run(config_path,genome_path)
