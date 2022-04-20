from __future__ import print_function
import os
import neat
import random
import visualize

# 2-input XOR inputs and expected outputs.
# xor_inputs = [(0.0, 0.0), (0.0, 1.0), (1.0, 0.0), (1.0, 1.0)]
# xor_outputs = [   (0.0,),     (1.0,),     (1.0,),     (0.0,)]

def coinflip(amount):
    result = 0
    for _ in range(amount):
        if random.random() > .5:
            result += 1
    return result

def eval_genome(genome,config):
    genome.fitness = 0
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    for i in range(10000):
        x = random.randint(5,15)
        guess = random.randint(0,x)
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
#
# def eval_genomes(genomes, config):
#     for genome_id, genome in genomes:
#         genome.fitness = 0
#         # genome.fitness = 4.0
#         net = neat.nn.FeedForwardNetwork.create(genome, config)
#         for i in range(1000):
#             x = random.randint(5,15)
#             guess = random.randint(0,x)
#             flips = coinflip(x)
#             output = net.activate((x,guess) )
#             end_index = output.index(max(output))
#             if end_index == 0:
#                 if flips>=guess:
#                     genome.fitness += 1
#                 # this will be calling good
#             else:
#                 if flips < guess:
#                     genome.fitness += 1
                # this is calling bad
            # genome.fitness -= min(1,((output[0]-flips)**2)/(1+flips))
            # genome.fitness += ((output[0]-flips)**2)/x

        # for xi, xo in zip(xor_inputs, xor_outputs):
            # output = net.activate(xi)
            # genome.fitness -= (output[0] - xo[0]) ** 2


def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5,filename_prefix="HighLowCheckpoint-"))

    # Run for up to 300 generations.

    pe = neat.ParallelEvaluator(16, eval_genome)
    winner = p.run(pe.evaluate, 5)
    # winner = p.run(eval_genomes, 10)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    # print('\nOutput:')
    # winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    # for xi, xo in zip(xor_inputs, xor_outputs):
        # output = winner_net.activate(xi)
        # print("input {!r}, expected output {!r}, got {!r}".format(xi, xo, output))

    # node_names = {-1:'A', -2: 'B', 0:'A XOR B'}
    # visualize.draw_net(config, winner, True, node_names=node_names)
    visualize.plot_stats(stats, ylog=False, view=True)
    # visualize.plot_species(stats, view=True)

    # p = neat.Checkpointer.restore_checkpoint('HighLowCheckpoint-4')
    # pe = neat.ParallelEvaluator(4, eval_genome)
    # winner = p.run(eval_genomes,1)
    # print(p)
    # pe = neat.ParallelEvaluator(4, eval_genome)
    # winner = p.run(pe.evaluate, 10)
    # print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config')
    run(config_path)
