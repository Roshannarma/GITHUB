# from __future__ import print_function
import os
import neat
# import random
# import visualize
import game
import pickle
import CustomGenome
import ConfigGenome
# import multiprocessing
# import time
# from functools import partial

LOCALDIR = os.path.dirname(__file__)






def run(config_file):

    config = neat.Config(CustomGenome.CustomGenome , neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)



    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # local_dir = os.path.dirname(__file__)
    config_path = os.path.join(LOCALDIR, 'checkpoints\\CHK-')
    p.add_reporter(neat.Checkpointer(5,filename_prefix=config_path))
    ITERATIONS = int(input("What number of iterations do you want?:\n"))
    # ITERATIONS = 15

    winner = p.run(game.eval_genomes, ITERATIONS)

    print('\nBest genome:\n{!s}'.format(winner))

    # local_dir = os.path.dirname(__file__)
    finalPath = os.path.join(LOCALDIR,f"results\\winner{ITERATIONS}.pkl")
    # config_path = os.path.join(local_dir, 'config')


    with open(finalPath, "wb") as f:
        pickle.dump(winner, f)
        f.close()

    # print('\nBest genome:\n{!s}'.format(winner))

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    # local_dir = os.path.dirname(__file__)
    config_path = os.path.join(LOCALDIR, 'config')
    run(config_path)
