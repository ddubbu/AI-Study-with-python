class DefineTurn:
    def __init__(self, turn):
        self.turn = turn
    def enemy(self):
        if (self.turn == "X"):
            return "O"
        else:
            return "X"


turn = DefineTurn("X")
print("turn is", turn.turn, "enemy is", turn.enemy())


