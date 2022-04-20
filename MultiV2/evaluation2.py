import multiprocessing
from functools import partial
import neat
import generation as gp
import time

COINS = 5


def make_action(Player,roundInfo,gameInfo):
    if roundInfo["currentBetPlayer"] == Player["id"] and roundInfo["passCount"] > 0:
        roundInfo["roundDict"]["roundEnd"] = True
        roundInfo["roundDict"]["roundLost"] = False
        roundInfo["roundDict"]["roundEnder"] = Player["id"]
        return roundInfo


    net = Player["neural"]
    output = net.activate((Player["headCount"],Player["currentCoins"],
                           roundInfo["passCount"], roundInfo["currentBet"],
                           roundInfo["totalCounts"],gameInfo["playersAlive"]))

    end_index = output.index(max(output))
    # print(f"choice : {end_index}")

    if end_index == 0:
        # print(f"PassCount: {roundInfo['passCount']}")
        # print(f"CurrentBetPlayer: {roundInfo['currentBetPlayer']}")
        # print(f"Player: {Player}")
        roundInfo["passCount"]+=1
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

#
# def countPlayersAlive(Players):
#     playersAlive = 0
#     for i in range(len(Players)):
#         if Players[i]["alive"]:
#             playersAlive += 1
#     if(playersAlive == 0):
#         print(Players)
#         3 + "sd"
#     print(playersAlive)


def play_round(Players,roundInfo,gameInfo):
    i = gameInfo["StartingID"] -1
    while True:
        # print("play_round")
        i = (i+1)%len(Players)
        # roundInfo["roundDict"]["roundEnd"] = True
        # roundInfo["roundDict"]["roundWon"] = True
        # roundInfo["roundDict"]["roundEnder"] = 0
        # countPlayersAlive(Players)
        # time.sleep(1)
        if Players[i]["alive"]:
            roundInfo = make_action(Players[i],roundInfo,gameInfo)
            # print(f"Alive: {Players[i]}")
        else:

            # print(f"Dead: {Players[i]}")
            continue
        if roundInfo["roundDict"]["roundEnd"]:
            return roundInfo




def play_game(Players,gameInfo):
    while True:
        # print("play_game")
        roundInfo = gp.round(Players,gameInfo["StartingID"])
        roundInfo = play_round(Players,roundInfo,gameInfo)
        if roundInfo["roundDict"]["roundEnd"]:
            id = roundInfo["roundDict"]["roundEnder"]
            # print(roundInfo)
            if roundInfo["roundDict"]["roundLost"]:
                Players[id]["currentCoins"] -= 1
                # for i in range(len(Players)):
                #     if i!=id:
                #         Players[i]["currentCoins"] -= 1
            else:
                for i in range(len(Players)):
                    if i!=id:
                        Players[i]["currentCoins"] -= 1
            # gameInfo["StartingID"] = gp.findAlive(Players,id)
            Players,gameInfo = gp.removeDeadPlayers(Players,gameInfo)
            gameInfo["StartingID"] = gp.findAlive(Players,id)
            # print(Players)
            # print(gameInfo)
            # time.sleep(1)
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
    for _ in range(100):
        Players = gp.resetPlayers(Players,COINS)
        gameInfo = gp.game(Players,order)
        gameInfo = play_game(Players,gameInfo)
        if gameInfo["gameDict"]["gameEnd"]:
            id = gameInfo["gameDict"]["gameWinner"]
            scoreList[id] += 1
        else:
            print("houston we have a problem about: eval_group")


    # i = 0
    for i in range(len(genomes)):
        genomes[i][1].fitness = scoreList[i]
    # for genome_id,genome in genomes:
        # genome.fitness = scoreList[i]
        # i += 1
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
            genome.fitness += 100
        # for genome_id,genome in WinnersBracket:
        #     genome.fitness = 100
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
            genome.fitness += 100
        # for genome_id,genome in WinnersBracket:
        #     genome.fitness = 200
            # print(genome.fitness)
            # print(genome.fitness)
        # print(genomeChunk)

    numGenomes = len(genomes)
    for i in range(0, len(genomeChunks), 1):
        for x in range(0,chunk_size,1):
            if numGenomes <= (chunk_size*i)+x:
                break
            genomes[(chunk_size*i)+x][1].fitness = genomeChunks[i][x][1].fitness
    # print("finished chunk")

    return genomes


# if __name__ == "__main__":
