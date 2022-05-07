import random
import neat
from numba import jit,cuda
import timeit

# @jit(nopython=True)
def rollDice(amount):
    diceList = [0]*6
    for _ in range(amount):
        num = random.randint(0,5)
        diceList[num] += 1
    return diceList

# @jit(nopython=True)
# def rollDiceFast(amount):
#     diceList = [0]*6
#     for _ in range(amount):
#         num = random.randint(0,5)
#         diceList[num] += 1
#     return diceList


# %timeit rollDice(6)

# %timeit rollDiceFast(6)


def player(genome,config,amount,id):
    return {
    "id":id,
    "currentDice" : rollDice(amount),
    "numDice":amount,
    "alive":True,
    "neural":neat.nn.FeedForwardNetwork.create(genome, config),
    }



def resetPlayer(player,amount):
    player["numDice"] = amount
    player["currentDice"] = rollDice(amount)
    player["alive"] = True
    return player

def resetPlayers(players,amount):
    return {k:resetPlayer(v,amount) for k,v in players.items()}

# players = {0:player(1,1,3,0),1:player(1,1,5,1)}
# resetPlayers(players,5)

def rerollPlayer(player):
    player["currentDICE"] = rollDice(player["numDice"])
    return player

def rerollPlayers(players):
    return {k:rerollPlayer(player) for k,player in players.items()}

def findAlive(players, startID):
    numPlayers = len(players)
    for i in range(numPlayers):
        id = (startID + i) % numPlayers
        if players[id]["alive"]:
            return id
    raise Exception("There should be one player alive")

def removeDeadPlayers(players, gameInfo):
    alive, winner = 0, -1
    for k,player in players.items():
        if (player["numDice"] <= 0):
            player["alive"] = False
        else:
            alive += 1
            winner = k
    if alive == 1:
        gameInfo["result"]["end"] = True
        gameInfo["result"]["winner"] = winner
    return (players, gameInfo)

# players = {0:player(1,1,3,0),1:player(1,1,5,1)}
# round(players,0)

def round(players,startID):
    numPlayers = len(players)
    diceList = [0]*6
    for k,player in players.items():
        # print(player["currentDice"])
        diceList = [sum(i) for i in zip(player["currentDice"],diceList)]
        # print(diceList)
    return {
        "dice":{i+1:value for i,value in enumerate(diceList)},
        "result":{
        "end":False,
        "lost":False,
        "ender":-1
        },
        "betNumber":-1,
        "betPip": -1,
        "betPlayer": -1,
        "totalDice" : sum(diceList),
        "playersAlive": sum([ (player["alive"] if 1 else 0) for k,player in players.items()])
    }

def game(players,startID):
    return{
        "startID": startID,
        "playersAlive" : len(players),
        "result":{
        "end":False,
        "winner":-1
        }
    }
