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
        "info":{"headCount":coinflip(amount),"wins":0,"id":id},
        "neural":neat.nn.FeedForwardNetwork.create(genome, config),
    }

def rerollPlayer(Player,amount):
    Player["info"]["headCount"] = coinflip(amount)
    return Player
    # return {
    #     "info":{"headCount":coinflip(amount)},
    #     "neural":Player["Neural"],
    #     "wins":Player["wins"]
    # }

def game(Players,initialId):
    totalHeads = 0
    for i in range(4):
        totalHeads += Players[i]["info"]["headCount"]
    return{
    "passCount":0,
    "currentBet":1,
    "gameEnd":{"end":False},
    "totalHeads" : totalHeads,
    "currentBetPlayer":initialId
    }
