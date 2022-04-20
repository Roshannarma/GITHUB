import multiprocessing
# import time
from functools import partial
import neat
import generation as gp

COINS = 5
MAX_PLAYERS = 4



def make_action(Player,gameInfo):
    if gameInfo["currentBetPlayer"]==Player["info"]["id"] and gameInfo["passCount"] > 0:
        gameInfo["gameEnd"]["end"] = True
        gameInfo["gameEnd"]["curPlayerwins"] = True
        gameInfo["gameEnd"]["curPlayer"] = Player["info"]["id"]
        return gameInfo
    net = Player["neural"]
    output = net.activate((Player["info"]["headCount"],gameInfo["passCount"],gameInfo["currentBet"]))
    end_index = output.index(max(output))
    if end_index == 0:
        gameInfo["passCount"]+=1
        return gameInfo
    elif end_index == 1:
        gameInfo["currentBet"] += 1
        if gameInfo["currentBet"] > (COINS*MAX_PLAYERS):
            gameInfo["gameEnd"]["end"] = True
            gameInfo["gameEnd"]["curPlayerwins"] = False
            gameInfo["gameEnd"]["curPlayer"] = Player["info"]["id"]
            return gameInfo
        gameInfo["passCount"] = 0
        gameInfo["currentBetPlayer"] = Player["info"]["id"]
        return gameInfo
    elif end_index == 2:
        if(gameInfo["currentBet"] > gameInfo["totalHeads"]):
            gameInfo["gameEnd"]["end"] = True
            gameInfo["gameEnd"]["curPlayerwins"] = True
            gameInfo["gameEnd"]["curPlayer"] = Player["info"]["id"]
        else:
            gameInfo["gameEnd"]["end"] = True
            gameInfo["gameEnd"]["curPlayerwins"] = True
            gameInfo["gameEnd"]["curPlayer"] = gameInfo["currentBetPlayer"]
        return gameInfo
    else:
        print("it should never come here, we have a big problem")
        time.sleep(10)
        return {"error":"Extra Output obtained"}

def play_round(order,gameInfo):
    i = order["start"]
    while True:
        i = i%4
        gameInfo = make_action(order["Players"][i],gameInfo)
        if "error" in gameInfo:
            return gameInfo
        if gameInfo["gameEnd"]["end"]:
            # print(gameInfo["gameEnd"])
            return gameInfo
        i+=1

def eval_group(genomes,config):

    # print(len(genomes))
    try:
        Player0 = gp.player(genomes[0][1],config,COINS,0)
        Player1 = gp.player(genomes[1][1],config,COINS,1)
        Player2 = gp.player(genomes[2][1],config,COINS,2)
        Player3 = gp.player(genomes[3][1],config,COINS,3)
    except:
        print(genomes)
        print(genomes[0])
        print(genomes[1])
        print(genomes[2])
        print(genomes[3])



    order = {
    "start":0,
    "Players" : {
    0:Player0,
    1:Player1,
    2:Player2,
    3:Player3,
        }
    }



    # while True:
    for _ in range(1000):
        gameInfo = gp.game(order["Players"],(order["start"]-1)%4)
        result = play_round(order,gameInfo)
        if "error" in result:
            print(result["error"])
            break
        if gameInfo["gameEnd"]["curPlayerwins"]:
            id = gameInfo["gameEnd"]["curPlayer"]
            order["Players"][id]["info"]["wins"] += 1
            order["start"] = id+1
        else:
            id = gameInfo["gameEnd"]["curPlayer"]
            order["Players"][id]["info"]["wins"] -= 1
            # for id in range(4):
                # if id != gameInfo["gameEnd"]["curPlayer"]:
                    # order["Players"][id]["info"]["wins"] += 1
            order["start"] = id+1
        for id in range(4):
            order["Players"][id] = gp.rerollPlayer(order["Players"][id],COINS)

    for id in range(4):
        genomes[id][1].fitness = order["Players"][id]["info"]["wins"]
        # print(genomes[id][1].fitness)
    return [genomes,config]

def eval_genomes(genomes,config):
    genomes = genomes[0:64]
    genomeChunks = []
    chunk_size = 4
    for i in range(0, len(genomes), chunk_size):
        genomeChunks.append(genomes[i:i+chunk_size])
    part_group = partial(eval_group,config=config)
    try:
        pool = multiprocessing.Pool()
        genomeChunks = pool.map(part_group,genomeChunks)
        pool.close()
    except:
        print(genomes)
        print(genomeChunks)
    for i in range(0, len(genomeChunks), 1):
        for x in range(0,chunk_size,1):
            genomes[(chunk_size*i)+x][1].fitness = genomeChunks[i][0][x][1].fitness
