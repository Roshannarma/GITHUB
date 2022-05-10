from __future__ import print_function
import os
import neat
import random
import visualize
# import evaluation
import pickle
LOCALDIR = os.path.dirname(__file__)
import game

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



def run(config_file):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    ITERATIONS = int(input("What number of iterations do you want?:\n"))
    config_path = os.path.join(LOCALDIR, 'checkpoints\\CHK-')

    p = neat.Checkpointer.restore_checkpoint(config_path + str(ITERATIONS))
    winner = p.run(game.eval_genomes, 1)

    finalPath = os.path.join(LOCALDIR,f"results\\winner{ITERATIONS}.pkl")


    with open(finalPath, "wb") as f:
        pickle.dump(winner, f)
        f.close()


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(LOCALDIR, 'config')
    # ITERATIONS = int(input("What number of iterations do you want?:\n"))
    # genome_path = os.path.join(LOCALDIR,f"results\\winner{ITERATIONS}.pkl")
    run(config_path)
