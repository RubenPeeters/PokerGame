from PokerAI import Simulator
class Bot:
    def __init__(self,amount):
        self.amount_of_money = amount
        self.hand = {}
        self.move = 0
        self.diff = 0
        self.diffs = "Normal"
    def set_diff(self,diff):
        self.diff = diff
        if diff == 0.1:
            self.diffs ="Easy"
        elif diff ==0.15:
            self.diffs ="Normal"
        elif diff == 0.2:
            self.diffs = "Hard"
    def get_move(self):
        return self.move

    def calc_move(self, hand, table):
        sim = Simulator(hand, table, 100)
        chance = sim.calculate_chance()
        if chance >= 0.6 + self.diff:
            self.move = "Raise"
        elif chance >= 0.4 + self.diff/2:
            self.move = "Call/Check"
        else:
            self.move = "Fold"

    def get_Move(self):
        return self.move

testhand = {0: "C4", 1: "H7"}
testtable = {0: "C2", 1: "S7", 2: "CA", 3: "S9", 4: "C3"}