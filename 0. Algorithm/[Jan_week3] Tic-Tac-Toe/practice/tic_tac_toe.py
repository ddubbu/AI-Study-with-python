# class DefineTurn:
#     def __init__(self, turn):
#         self.turn = turn
#     def enemy(self):
#         if (self.turn == "X"):
#             return "O"
#         else:
#             return "X"
#
#
# turn = DefineTurn("X")
# print("turn is", turn.turn, "enemy is", turn.enemy())


class Map:
    play = 0

    def __init__(self, map):
        self.map = map

    def draw_map(self):
        # print each case map
        for row in range(0, 3):  # 행 탐색 iterator
            for col in range(0, 3):  # 열 탐색 iterator
                print(map[row][col], end=" ")
            print("")  # print("\n") 이면 한줄이 더 추가로 띄어지던데

    def inc_play(self):
        self.play = self.play + 1

map = Map([[1,2,3],[4,5,6],[7,8,9]])
map.inc_play()
print(map.play)