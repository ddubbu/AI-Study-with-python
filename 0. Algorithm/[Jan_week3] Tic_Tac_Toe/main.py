class Map:
    def __init__(self, map_init):
        self.status = map_init  # 현재 돌 위치 지도 갱신
        self.turn = ""  # 항상 'X' 먼저
        self.round = 1
        self.total_stones = 0
        self.setting()  # self.turn , self

    def setting(self):
        # init method 내에서 숨겨서 초기화
        # self.turn 과 self.total_stones 를 갱신한다.
        x_count = 0
        o_count = 0
        for row in range(0, 3):  # 행 탐색 iterator
            for col in range(0, 3):  # 열 탐색 iterator
                if self.status[row][col][0] == 'X':
                    x_count = x_count + 1
                elif self.status[row][col][0] == 'O':
                    o_count = o_count + 1
        if x_count <= o_count:
            self.turn = "X"
        else:
            self.turn = "O"

        self.total_stones = x_count + o_count

    def draw_map(self):
        # print each case map
        for row in range(0, 3):  # 행 탐색 iterator
            for col in range(0, 3):  # 열 탐색 iterator
                print(self.status[row][col], end=" ")
            print("") # print("\n") 이면 한줄이 더 추가로 띄어지던데

    def inc_round(self):
        self.round = self.round + 1
        self.total_stones = self.total_stones + 1

    def update_map(self, where): # map 에 새로운 수를 넣자 마자 play 횟수, turn 자동 갱신
        self.status[where[0]][where[1]] = self.turn + str(self.round)
        self.draw_map()
        self.inc_round()
        self.next_turn()

    def enemy(self):
        if self.turn == "X":
            return "O"
        else:
            return "X"

    def next_turn(self):
        if self.turn == "X":
            self.turn = "O"
        else:
            self.turn = "X"


def main():
    # set read/write file variables
    rfile = open("input.txt", mode="r")
    wfile = open("output.txt", mode="wt", encoding="utf-8")

    # read each lines
    rlines = rfile.readlines()

    # the first line has (total) the number of case
    totalCase = int(rlines[0])

    # iterative each Case
    # 1. make map
    for case in range(1, totalCase + 1):
        # initialize
        map_init = [['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]

        # push elements
        for row in range(0, 3):  # 행 탐색 iterator
            line = rlines[(case-1)*3+(row+1)].split(" ")
            line[-1] = line[-1].replace("\n", "")  # 마지막 줄바꿈 없애기
            for col in range(0, 3):  # 열 탐색 iterator
                map_init[row][col] = line[col] + "s"  # setting turn 기록

        # declare object with
        map = Map(map_init)

        # print each case map
        print("----------")
        print("Case #%d"%case)
        map.draw_map()

        winner = ""
        end_result = ["X", "O", "TIE"]
        # 예외상황 처리
        if map.total_stones == 0 or map.total_stones == 1:
            winner = "TIE"  # 볼 것도 없이 무승부 (확실함)
        # elif map.total_stones == 9:
        #     result = "The End"
        #     # 결과 판독하고 나서

        else:
            winner = is_bingo(map)[0]
            while not winner:
                if map.total_stones == 9:
                    result = "TIE"
                    break  # 끝
                # else
                print(">>>> play ROUND", map.round)
                optimal_move(map)
                winner = is_bingo(map)[0]

            # if is_bingo(map)[0] == "X" or is_bingo(map)[0] == "O": # bingo 발생했다
            #     result = is_bingo(map)[0]
        print("result :", winner)
        if is_bingo(map)[0] == "X" or is_bingo(map)[0] == "O": # bingo 발생했다
            print("BINGO !!", is_bingo(map)[1])
        wLines = winner + "\n"  # 사실 count 는 len(jumpList)로도 가능
        wfile.writelines([wLines])

    wfile.close()
    print("========\n confirm output.txt file")

def optimal_move(map):  # min-max algorithm
    x_best_score = -10
    o_best_score = -10
    where = []  # memorize move list

    # 참조 코드에서는 "X" 시작을 우선으로 하네.
    # 그러므로 turn에 따라 scores 판을 바꿔야 하구나!! 대박!
    x_scores = {
        "X": 1,
        "O": -1,
        "TIE": 0
    }

    o_scores = {
        "O": 1,
        "X": -1,
        "TIE": 0
    }

    for row in range(0, 3):
        for col in range(0, 3):
            if map.status[row][col] == ".s":
                # 임시방편 바꿔놓기
                map.status[row][col] = map.turn + str(map.round)
                map.next_turn()  # turn 도 갱신되어야해!
                if(map.turn == "O"):
                    score = minimax(map, 0, False, x_scores)
                    map.status[row][col] = ".s"  # 제자리
                    if score > x_best_score:
                        x_best_score = score
                        where = [row, col]  # change
                elif(map.turn == "X"):
                    score = minimax(map, 0, False, o_scores)
                    map.status[row][col] = ".s"  # 제자리
                    if score > o_best_score:
                        o_best_score = score
                        where = [row, col]  # change

                map.next_turn()  # turn 복귀

    # 최고의 수를 찾은 다음에
    print("--> optimal move", where)
    map.update_map(where)

    return  # end


def minimax(map, depth, is_maximizing, mini_scores):
    result_lsit = ["X", "O", "TIE"]
    result = is_bingo(map)  #check that is there winner?
    if result[0] in result_lsit:
        return mini_scores[result[0]]

    # else continue 탐색
    if is_maximizing:
        best_score = -10
        for row in range(0,3):
            for col in range(0,3):
                if map.status[row][col] == ".s":
                    # 임시방편 바꿔놓기
                    map.status[row][col] = map.turn + str(map.round)
                    map.next_turn()  # turn 도 갱신되어야해!
                    score = minimax(map, depth + 1, False, mini_scores)
                    map.status[row][col] = ".s" # 제자리
                    map.next_turn()  # turn 복귀
                    best_score = max(score, best_score)
        return best_score

    else:
        best_score = 10
        for row in range(0, 3):
            for col in range(0, 3):
                if map.status[row][col] == ".s":
                    # 임시방편 바꿔놓기
                    map.status[row][col] = map.turn + str(map.round)
                    map.next_turn()
                    score = minimax(map, depth + 1, True, mini_scores)
                    map.status[row][col] = ".s"  # 제자리
                    map.next_turn()
                    best_score = min(score, best_score)
        return best_score

def is_bingo(map):
    # 3 연속 빙고 있어?

    m = map.status
    # row check
    for row in range(0, 3):
        if m[row][0][0] != ".":  # 점 아닌데 다 같다
            if m[row][0][0] == m[row][1][0] and m[row][1][0] == m[row][2][0]:
                return [m[row][0][0], "r" + str(row)]

    # col check
    for col in range(0, 3):
        if m[0][col][0] != ".":
            if m[0][col][0] == m[1][col][0] and m[1][col][0] == m[2][col][0]:
                return [m[0][col][0], "c" + str(col)]

    # 대각선(diagonal) check
    # (d0) 왼쪽 -> 오른쪽 [[0,0], [1,1], [2,2]]

    if m[0][0][0] != "." and m[0][0][0] == m[1][1][0] and m[1][1][0] == m[2][2][0]:
        return [m[0][0][0], "d0"]

    # (d1) 오른쪽 -> 왼쪽 [[2,0], [1,1], [0,2]]
    if m[2][0][0] != "." and m[2][0][0] == m[1][1][0] and m[1][1][0] == m[0][2][0]:
        return [m[2][0][0], "d1"]

    # if winner == None
    openSpots = 0
    for row in range(0, 3):
        for col in range(0, 3):
            if m[row][col] == ".s":
                openSpots += 1

    if openSpots == 0:
        return ["TIE", ""]
    else:
        return [None, ""]  # 빙고도 없고 꽉찬 상태도 아니므로 mini-, maxi-mize 계속

main()