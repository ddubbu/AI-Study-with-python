class DefineTurn:
    def __init__(self, turn):
        self.turn = turn
    def enemy(self):
        if (self.turn == "X"):
            return "O"
        else:
            return "X"



def main():
    # set read/write file variables
    rfile = open("input.txt", mode="r")
    wfile = open("output.txt", mode="wt", encoding="utf-8")

    # read each lines
    rlines = rfile.readlines()

    # the first line has (total) the number of case
    totalCase = int(rlines[0])

    # iterative each Case
    # make map each case.
    for case in range(1, totalCase +1):
        #global case
        # initialize
        map_cur = [ ['.','.','.'], ['.', '.', '.'], ['.', '.', '.']]

        # push elements
        for row in range(0,3): # 행 탐색 iterator
            line = rlines[(case-1)*3+(row+1)].split(" ")
            line[-1] = line[-1].replace("\n", "")  # 마지막 줄바꿈 없애기
            for col in range(0,3): # 열 탐색 iterator
                map_cur[row][col] = line[col] + "s"  # setting turn 기록

        # print each case map
        print("----------")
        print("Case #%d"%case)
        for row in range(0, 3):  # 행 탐색 iterator
            for col in range(0, 3):  # 열 탐색 iterator
                print(map_cur[row][col], end=" ")
            print("") # print("\n") 이면 한줄이 더 추가로 띄어지던데
        # print map simply
        # for row in range(0,3):
        #     print(map_cur[row])

        # who's turn?
        turn_count = who_turn(map_cur)
        turn = ""
        result = ""

        # 예외상황 처리
        if(turn_count == 1 or turn_count == 0):
            result = "TIE"  # 볼 것도 없이 무승부
        elif(turn_count == 9):
            result = "The End"
            # 결과 판독하고 나서

        else:
            if(turn_count % 2 == 1) : # 놓아진 돌이 홀수 개이면, 'O' 차례
                turn = "O"
                result = play_game(map_cur, turn)
            else :
                turn = "X"
                result = play_game(map_cur, turn)

        print("result :", result)

def who_turn(map_cur):
    # 항상 'x' 먼저
    # x_count = 0
    # o_count = 0
    #
    # for row in range(0,3): # 행 탐색 iterator
    #     for col in range(0,3): # 열 탐색 iterator
    #         if(map_cur[row][col][0] == 'X'):
    #             x_count  = x_count + 1
    #         elif(map_cur[row][col][0] == 'O'):
    #             o_count  = o_count + 1
    # if(x_count <= o_count):
    #     return 'X' # I want to change this to number, 0
    # else:
    #     return 'O'

    count = 0
    for row in range(0, 3):  # 행 탐색 iterator
        for col in range(0, 3):  # 열 탐색 iterator
            if(map_cur[row][col][0] == "."):
                continue
            else:
                count = count + 1
    return count

def play_game(map_cur, turn):
    print("play now")
    # 1. 바로 이기는 공격 유무 확인
    # 현재 turn 의 돌이 연속(혹은 띄어서) 2개인지를 확인한다.
    my2series = check2series(map_cur, turn)
    if(my2series[0]):
        print("BINGO!!", my2series)
        return turn

    # 2. 방어할 곳 확인
    t = DefineTurn(turn)
    print("turn is", t.turn, "enemy is", t.enemy())


def check2series(map_cur, turn):

    # result is list 형태 [존재함, 어느 줄 빙고?] 예로, [1, "r1"] r1에서 빙고해서 이길 것임
    t = DefineTurn(turn)

    # row check
    for row in range(0, 3):  # 행 탐색 iterator ※ 중간까지만 확인해도 됨.
        for col in range(0, 2):  # 열 탐색 iterator
            if(map_cur[row][col][0] == turn):
                if(map_cur[row][(col+1)%3][0] == turn and map_cur[row][(col+2)%3][0] != t.enemy()):
                    # 이미 Game Over 인 상태 (already 3 빙고) 끝 은 없는 걸로
                    return [1, "r" + str(row)]
                elif(map_cur[row][(col+2)%3][0] == turn and map_cur[row][(col+1)%3][0] != t.enemy()):
                    return [1, "r" + str(row)]

    # col check
    for row in range(0, 2):  # 행 탐색 iterator
        for col in range(0, 3):  # 열 탐색 iterator
            if(map_cur[row][col][0] == turn):
                if(map_cur[(row+1)%3][col][0] == turn and map_cur[(row+2)%3][col][0] != t.enemy()):
                    # 이미 Game over 인 상태(already 3 빙고) 끝 은 없는 걸로
                    return [1, "c" + str(col)]
                elif(map_cur[(row+2)%3][col][0] == turn and map_cur[(row+1)%3][col][0] != t.enemy()):
                    return [1, "c" + str(col)]


    # cross check
    cross1 = [[0,0], [1,1]]  # check only 2, ignore [2,2]]
    cross2 = [[0,2], [1,1]]  # check only 2, ignore [2,0]]

    for idx in cross1:
        if (map_cur[idx[0]][idx[1]][0] == turn) :
            if(map_cur[(idx[0]+1)%3][(idx[1]+1)%3][0] == turn and map_cur[(idx[0]+2)%3][(idx[1]+2)%3][0] != t.enemy()):
                return [1, "cross1"]
            elif(map_cur[(idx[0]+2)%3][(idx[1]+2)%3][0] == turn and map_cur[(idx[0]+1)%3][(idx[1]+1)%3][0] != t.enemy()):
                return [1, "cross1"]
    for idx in cross2:
        if (map_cur[idx[0]][idx[1]][0] == turn) :
            if(map_cur[(idx[0]+1)%3][(idx[1]-1)%3][0] == turn and map_cur[(idx[0]+2)%3][(idx[1]-2)%3][0] != t.enemy()):
                return [1, "cross2"]
            elif(map_cur[(idx[0]+2)%3][(idx[1]-2)%3][0] == turn and map_cur[(idx[0]+1)%3][(idx[1]-1)%3][0] != t.enemy()):
                return [1, "cross2"]

    return [0, ""]  # 2 Series 없으면


# main 함수 호출
main()
