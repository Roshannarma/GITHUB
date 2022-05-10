from player import Player
from dotted_dict import DottedDict
from diceRound import diceRound


class diceGame():
    def __init__(self,numPlayers,names=[],max_iteration=2**15):
        self.numPlayers = numPlayers
        self.players = []
        for i in range(len(names)):
            self.players.append(Player(names[i]))
        for i in range(self.numPlayers-len(names)):
            self.players.append(Player(f"bot-{i}"))
        self.totalPlayers = self.players
        self.max_iteration = max_iteration
        self.round = diceRound(self.players)


    def printout(self):
        pass

    def removeDead(self, players):
        playerList = [i for i in players if i.alive()]
        self.numPlayers = len(playerList)
        # print(playerList)
        return playerList


    def run(self):
        for i in range(self.max_iteration):
            self.step()
            if self.numPlayers == 1:
                return self.players
        raise Exception("runtime error, infinite loop")

    def reroll(self):
        for i in self.players:
            i.resetPlayer()

    def step(self):
        self.round.step()
        if not self.round.done:
            return
        self.players = self.removeDead(self.round.players)
        self.reroll()
        self.round = diceRound(self.players)



game = diceGame(numPlayers = 2,names=["Roshan"])
game.run()
