from player import Player
from dotted_dict import DottedDict

RAISE = 0
CHALLENGE = 1
EXACT = 2

class diceRound():

    def __init__(self,players):
        self.players = players
        self.done = False
        self.hiddenInfo = DottedDict({
            "diceValues":[0,0,0,0,0,0]
        })
        self.visibleInfo = DottedDict({
            "numPlayers":len(self.players),
            "playerNames":[],
            "curPlayer":0,
            "totalDice":0,
            "pip":0,
            "value":0,
            "diceList":[],
            "prevBets":[]
        })
        self.populate()

    def populate(self):
        for i in range(self.visibleInfo.numPlayers):
            self.visibleInfo.totalDice += self.players[i].amount
            self.visibleInfo.playerNames.append(self.players[i].name)
            self.visibleInfo.diceList.append(self.players[i].amount)
            for j in range(6):
                self.hiddenInfo.diceValues[j] += self.players[i].diceList[j]


    def playerLose(self):
        self.players[self.visibleInfo.curPlayer].loseAmount()
        self.done = True

    def betPlayerLose(self):
        self.players[self.visibleInfo.curPlayer-1%(self.visibleInfo.numPlayers)].loseAmount()
        self.done = True

    def playerWin(self):
        for i in range(self.visibleInfo.numPlayers):
            if i != self.players.curPlayer:
                self.players[i].loseAmount()
        self.done = True


    def step(self):
        # print(self.players)
        # print(self.visibleInfo.curPlayer)
        action,actionInfo = self.players[self.visibleInfo.curPlayer].getInput(self.visibleInfo)


        if not (0 <= action < 3 and 0 <= actionInfo.pip < 6 and 1 <= actionInfo.value < self.visibleInfo.totalDice+1):
            self.playerLose()
            return

        if action == RAISE:
            if self.visibleInfo.pip <= actionInfo.pip and self.visibleInfo.value >= actionInfo.value:
                self.playerLose()
                return
            elif self.visibleInfo.pip > actionInfo.pip and self.visibleInfo.value > actionInfo.value:
                self.playerLose()
                return


            self.visibleInfo.value = actionInfo.value
            self.visibleInfo.pip = actionInfo.pip
            self.visibleInfo.curPlayer = (self.visibleInfo.curPlayer + 1) % (self.visibleInfo.numPlayers)

        elif action == CHALLENGE:
            if self.visibleInfo.value <= self.hiddenInfo.diceValues[self.visibleInfo.pip]:
                self.playerLose()
            else:
                self.betPlayerLose()

        else: # this is always going to be exact
            if self.visibleInfo.value != self.hiddenInfo.diceValues[self.visibleInfo.pip]:
                self.playerLose()
            else:
                self.playerWin()
        return


from dotted_dict import DottedDict
