import random
from dotted_dict import DottedDict

def rollDice(amount):
    diceList = [0,0,0,0,0,0]
    for _ in range(amount):
        num = random.randint(0,5)
        diceList[num] += 1
    return diceList


class Player():
    def __init__(self, name):
        self.amount = 5
        self.diceList = rollDice(self.amount)
        self.actionSpaces = 3
        self.name = name

    def loseAmount(self):
        if self.amount <= 0:
            raise Exception("Amount is too low initially")
        self.amount -= 1

    def resetPlayer(self):
        self.diceList = rollDice(self.amount)

    def displayGameState(self,info):
        print(self.name)
        print(info)
        print(self.diceList)


    def getInteger(self,number,prompt):
        while(1):
            try:
                value = int(input(prompt))

                if 0 > value or value > number:
                    raise Exception("Invalid action")
                return value
            except:
                print(f"This input needs to be an integer between 0-{number}")



    def getInput(self, info):
        self.displayGameState(info)
        action = self.getInteger(2, "What action do you want to take?: ")

        if action == 0:
            actionInfo = DottedDict({
                "pip": self.getInteger(5,"What pip do you want to raise to?: "),
                "value": self.getInteger(info.totalDice, "What number of dice do you want to raise to?: ")
            })

            return (action,actionInfo)

        return (action,DottedDict({"pip":0,"value":1}))

    def alive(self):
        return self.amount != 0




if __name__ == "__main__":
    p = Player()
    # p.amount
    p.loseAmount()
    # p.amount
    p.getInput({"Bet":5,"pip":2,"betPlayer":"player2"})
