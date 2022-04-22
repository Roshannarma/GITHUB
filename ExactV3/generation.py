import random
import neat
def coinflip(amount):
    result = 0
    for _ in range(amount):
        if random.random() > .5:
            result += 1
    return result

def player(genome,config,amount,id):
    return {
        # "info":{
        "headCount":coinflip(amount),
        # "wins":0,
        "id":id,
        "currentCoins" :amount,
        "alive":True,
        # },
        "neural":neat.nn.FeedForwardNetwork.create(genome, config),
    }

def resetPlayers(Players,amount):
    for i in range(len(Players)):
        Players[i] = resetPlayer(Players[i],amount)
    return Players

def resetPlayer(Player,amount):
    Player["headCount"] = coinflip(amount)
    Player["currentCoins"] = amount
    Player["alive"] = True
    return Player

def rerollPlayer(Player):
    Player["headCount"] = coinflip(Player["currentCoins"])
    return Player

def game(Players,initialId):
    totalHeads = 0
    totalCounts = 0
    for i in range(len(Players)):
        totalHeads += Players[i]["headCount"]
        totalCounts += Players[i]["currentCoins"]
    return{
    "gameDict":{
    "gameEnd":False,
    "gameWinner":-1
    },
    "StartingID": initialId,
    "playersAlive" : len(Players)
    }

def round(Players,initialId):
    totalHeads = 0
    totalCounts = 0
    playersAlive = 0
    for i in range(len(Players)):
        totalHeads += Players[i]["headCount"]
        totalCounts += Players[i]["currentCoins"]
        playersAlive += Players[i]["alive"]
    return {
    "currentBet": 0,
    "totalHeads" : totalHeads,
    "totalCounts": totalCounts,
    "currentBetPlayer":initialId,
    "playersAlive" : playersAlive,
    "roundDict":{
    "roundEnd":False,
    "roundLost":False,
    "roundEnder":-1
    }

    }

def removeDeadPlayers(Players,gameInfo):
    alive = 0
    winner = -1
    for i in range(len(Players)):
        if Players[i]["currentCoins"] <= 0:
            Players[i]["alive"] = False
        else:
            alive += 1
            winner = i
    if alive==1:
        gameInfo["gameDict"]["gameEnd"] = True
        gameInfo["gameDict"]["gameWinner"] = winner
    return (Players,gameInfo)


def findAlive(Players,startID):
    for i in range(len(Players)):
        id = (startID+i)%len(Players)
        if Players[id]["alive"]:
            return id
    print("this broke")
    3+"ts"
