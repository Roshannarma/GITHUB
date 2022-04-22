import multiprocessing
from functools import partial
import neat
import generation as gp
import time

COINS = 5


def make_action(Player,roundInfo,gameInfo):

    net = Player["neural"]
    output = net.activate((Player["headCount"],Player["currentCoins"],
                           roundInfo["currentBet"], roundInfo["totalCounts"],
                           gameInfo["playersAlive"]))

    end_index = output.index(max(output))

    if end_index == 0:
        if(roundInfo["currentBet"] == roundInfo["totalHeads"]):
            roundInfo["roundDict"]["roundEnd"] = True
            roundInfo["roundDict"]["roundLost"] = False
            roundInfo["roundDict"]["roundEnder"] = Player["id"]
        else:
            roundInfo["roundDict"]["roundEnd"] = True
            roundInfo["roundDict"]["roundLost"] = True
            roundInfo["roundDict"]["roundEnder"] = Player["id"]
        return roundInfo



    elif end_index == 1:
            roundInfo["currentBet"] += 1
            if roundInfo["currentBet"] > roundInfo["totalCounts"]:
                roundInfo["roundDict"]["roundEnd"] = True
                roundInfo["roundDict"]["roundLost"] = True
                roundInfo["roundDict"]["roundEnder"] = Player["id"]
                return roundInfo
            roundInfo["passCount"] = 0
            roundInfo["currentBetPlayer"] = Player["id"]
            return roundInfo


    elif end_index == 2:
        if(roundInfo["currentBet"] > roundInfo["totalHeads"]):
            roundInfo["roundDict"]["roundEnd"] = True
            roundInfo["roundDict"]["roundLost"] = True
            roundInfo["roundDict"]["roundEnder"] = roundInfo["currentBetPlayer"]
        else:
            roundInfo["roundDict"]["roundEnd"] = True
            roundInfo["roundDict"]["roundLost"] = True
            roundInfo["roundDict"]["roundEnder"] = Player["id"]
        return roundInfo
    else:
        print("it should never come here, we have a big problem")
        time.sleep(10)
        return {"error":"Extra Output obtained"}




def play_round(Players,roundInfo,gameInfo):
    i = gameInfo["StartingID"] -1
    while True:
        i = (i+1)%len(Players)

        if Players[i]["alive"]:
            roundInfo = make_action(Players[i],roundInfo,gameInfo)
        else:
            continue
        if roundInfo["roundDict"]["roundEnd"]:
            return roundInfo




def play_game(Players,gameInfo):
    while True:
        roundInfo = gp.round(Players,gameInfo["StartingID"])
        roundInfo = play_round(Players,roundInfo,gameInfo)
        if roundInfo["roundDict"]["roundEnd"]:
            id = roundInfo["roundDict"]["roundEnder"]
            if roundInfo["roundDict"]["roundLost"]:
                Players[id]["currentCoins"] -= 1
            else:
                for i in range(len(Players)):
                    if i!=id:
                        Players[i]["currentCoins"] -= 1
            Players,gameInfo = gp.removeDeadPlayers(Players,gameInfo)
            gameInfo["StartingID"] = gp.findAlive(Players,id)
            if gameInfo["gameDict"]["gameEnd"]:
                return gameInfo
            for id in range(len(Players)):
                Players[id] = gp.rerollPlayer(Players[id])

        else:
            print("houston we have a problem about: play_game")



def eval_group(genomes,config):

    Players = {}
    i = 0
    for genome_id,genome in genomes:
        Players[i] = gp.player(genome,config,COINS,i)
        i += 1
    order = 0
    scoreList = [0]*len(genomes)
    for _ in range(1000):
        Players = gp.resetPlayers(Players,COINS)
        gameInfo = gp.game(Players,order)
        gameInfo = play_game(Players,gameInfo)
        if gameInfo["gameDict"]["gameEnd"]:
            id = gameInfo["gameDict"]["gameWinner"]
            scoreList[id] += 1
        else:
            print("houston we have a problem about: eval_group")


    for i in range(len(genomes)):
        genomes[i][1].fitness = scoreList[i]
    return genomes



def eval_genomes(genomes,config):
    genomeChunks = []
    chunk_size = 4
    for i in range(0, len(genomes), chunk_size):
        genomeChunks.append(genomes[i:i+chunk_size])
    part_group = partial(eval_group,config=config)
    pool = multiprocessing.Pool()
    genomeChunks = pool.map(part_group,genomeChunks)
    pool.close()
    WinnersBracket = []
    if len(genomeChunks)>=16:
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
    elif len(genomeChunks)>=4:
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
    for i in range(0, len(genomeChunks), 1):
        for x in range(0,chunk_size,1):
            if numGenomes <= (chunk_size*i)+x:
                break
            genomes[(chunk_size*i)+x][1].fitness = genomeChunks[i][x][1].fitness

    return genomes
