import multiprocessing
from functools import partial
import neat
import generation as gp
import time
# from numba import jit


DICE = 5

PLAYERS = 4

VALUES = {0:"RAISE",1:"BS",2:"EXACT"}

# @jit(nopython=True)
def get_Output(player,roundInfo):
    net = player["neural"]
    outputList = []
    outputList.append(roundInfo["totalDice"])

    for i in range(0,6):
        outputList.append(player["currentDice"][i])

    outputList.append(roundInfo["playersAlive"])

    newList = [0]*6
    newList[roundInfo["betPip"]-1] = 1

    outputList += newList
    outputList.append(roundInfo["betNumber"])

    output = net.activate(outputList)
    return output


# @jit(nopython=True)
def make_action(player,roundInfo,gameInfo):
    output = get_Output(player, roundInfo)

    action = output.index(max(output[0:2]))
    if roundInfo["betPlayer"] == -1:
        action = 0
    # betPip = output.index(max(output[3:-1]))-2

    if (VALUES[action] == "RAISE"):
        betPip = output.index(max(output[3:-1]))-2
        # betNumber = round(20*output[-1])
        print(output)
        print(output[-1])
        betNumber = round(20*output[-1])
        # print(betNumber)
        # if(betNumber!=0 and betNumber != 20):
            # print(betNumber)

        if betNumber < roundInfo["betNumber"] or (betNumber == roundInfo["betNumber"] and betPip <= roundInfo["betPip"]):
            roundInfo["result"]["end"] = True
            roundInfo["result"]["lost"] = True
            roundInfo["result"]["ender"] = player["id"]
            return roundInfo

        roundInfo["currentBetPlayer"] = player["id"]
        roundInfo["betPip"] = betPip
        roundInfo["betNumber"] = betNumber
        return roundInfo

    elif (VALUES[action] == "BS"):
        if roundInfo["betNumber"] > roundInfo["dice"][roundInfo["betPip"]]:
            roundInfo["result"]["end"] = True
            roundInfo["result"]["lost"] = True
            roundInfo["result"]["ender"] = roundInfo["betPlayer"]
        else:
            roundInfo["result"]["end"] = True
            roundInfo["result"]["lost"] = True
            roundInfo["result"]["ender"] = player["id"]
        return roundInfo
    elif (VALUES[action] == "EXACT"):
        if roundInfo["betNumber"] == roundInfo["dice"][roundInfo["betPip"]]:
            roundInfo["result"]["end"] = True
            roundInfo["result"]["lost"] = False
            roundInfo["result"]["ender"] = player["id"]
        else:
            roundInfo["result"]["end"] = True
            roundInfo["result"]["lost"] = True
            roundInfo["result"]["ender"] = player["id"]
        return roundInfo
    else:
        raise Exception("The action is out of bounds")





# @jit(nopython=True)
def play_round(players,roundInfo,gameInfo):
    i = gameInfo["startID"] -1
    while True:
        i = (i+1)%len(players)

        if players[i]["alive"]:
            roundInfo = make_action(players[i],roundInfo,gameInfo)
        else:
            continue
        if roundInfo["result"]["end"]:
            return roundInfo


# @jit(nopython=True)
def play_game(players,gameInfo):
    while True:
        roundInfo = gp.round(players,gameInfo["startID"])
        roundInfo = play_round(players,roundInfo,gameInfo)
        if roundInfo["result"]["end"]:
            id = roundInfo["result"]["ender"]
            if roundInfo["result"]["lost"]:
                players[id]["numDice"] -= 1
            else:
                for i in range(len(players)):
                    if i!=id:
                        players[i]["numDice"] -= 1
            players,gameInfo = gp.removeDeadPlayers(players,gameInfo)
            gameInfo["startID"] = gp.findAlive(players,id)
            if gameInfo["result"]["end"]:
                return gameInfo
            players = gp.rerollPlayers(players)

        else:
            raise Exception("houston we have a problem about: play_game")

# @jit(nopython=True)
def eval_group(genomes,config):
    players = {}
    i = 0
    for genome_id,genome in genomes:
        players[i] = gp.player(genome,config,DICE,i)
        i += 1
    order = 0
    scoreList = [0]*len(genomes)
    for _ in range(1000):
        players = gp.resetPlayers(players,DICE)
        gameInfo = gp.game(players,order)
        gameInfo = play_game(players,gameInfo)
        if gameInfo["result"]["end"]:
            id = gameInfo["result"]["winner"]
            scoreList[id] += 1
        else:
            raise Exception("houston we have a problem about: eval_group")


    for i in range(len(genomes)):
        genomes[i][1].fitness = scoreList[i]
    return genomes



# @jit(nopython=True)
def eval_genomes(genomes,config):
    genomeChunks = []
    chunk_size = 4
    for i in range(0, len(genomes), chunk_size):
        genomeChunks.append(genomes[i:i+chunk_size])
    part_group = partial(eval_group,config=config)
    tempgenome = []
    for i in range(len(genomes)//chunk_size):
        tempgenome.append(part_group(genomeChunks[i]))
    genomeChunks = tempgenome
    # print(genomeChunks)
    # pool = multiprocessing.Pool()
    # genomeChunks = pool.map(part_group,genomeChunks)
    # pool.close()

    WinnersBracket = []
    if len(genomeChunks)>=2:
        for genomeChunk in genomeChunks:
            winner = -1
            value = 0
            loc = -1
            for genome_id,genome in genomeChunk:
                loc += 1
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
