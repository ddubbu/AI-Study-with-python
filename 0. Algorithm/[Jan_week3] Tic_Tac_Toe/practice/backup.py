
class Map():
    def __init__(self, map, turn, count):
        self.map = map
        self.play = 1
        self.turn = turn
        self.remain_play = 9-count
    def draw_map(self):
        # print each case map
        for row in range(0, 3):  # 행 탐색 iterator
            for col in range(0, 3):  # 열 탐색 iterator
                print(self.map[row][col], end=" ")
            print("") # print("\n") 이면 한줄이 더 추가로 띄어지던데

    def inc_play(self):
        self.play = self.play + 1
        self.remain_play = self.remain_play - 1

    def update_map(self, where): # map 에 새로운 수를 넣자 마자 play 횟수, turn 자동 갱신
        self.map[where[0]][where[1]] = self.turn + str(self.play)
        self.draw_map()
        self.inc_play()
        self.next_turn()

    def enemy(self):
        if (self.turn == "X"):
            return "O"
        else:
            return "X"
    def next_turn(self):
        if (self.turn == "X"):
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
    # make map each case.
    for case in range(1, totalCase +1):
        result = ""

        # initialize
        map_cur = [ ['.','.','.'], ['.', '.', '.'], ['.', '.', '.']]

        # push elements
        for row in range(0,3): # 행 탐색 iterator
            line = rlines[(case-1)*3+(row+1)].split(" ")
            line[-1] = line[-1].replace("\n", "")  # 마지막 줄바꿈 없애기
            for col in range(0,3): # 열 탐색 iterator
                map_cur[row][col] = line[col] + "s"  # setting turn 기록

        # who's turn?
        turn_count = who_turn(map_cur)

        # print each case map
        map = Map(map_cur, "", turn_count) # turn 멤버값 은 나중에 추가
        print("----------")
        print("Case #%d"%case)
        map.draw_map()
        print("remain Play is", map.remain_play)

        # 예외상황 처리
        if(turn_count == 0 or turn_count == 1 ):
            result = "TIE"  # 볼 것도 없이 무승부 (확실함)
        elif(turn_count == 9):
            result = "The End"
            # 결과 판독하고 나서

        else:
            if(turn_count % 2 == 1) : # 놓아진 돌이 홀수 개이면, 'O' 차례
                map.turn = "O"
                result = play_game(map)

                # ★☆★☆★☆★☆ 여기 recursive ★☆★☆★☆★☆
                if(result == "continue"):
                    play_game(map)

            else :
                map.turn = "X"
                result = play_game(map)

                # ★☆★☆★☆★☆ 여기 recursive ★☆★☆★☆★☆
                if(result == "continue"):
                    play_game(map)

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

def play_game(map):

    print("play now")

    # 1. 바로 이기는 공격 유무 확인
    # 현재 turn 의 돌이 연속(혹은 띄어서) 2개인지를 확인한다.
    my2series = check2series(map.map, map.turn)
    if(my2series[0]):
        print("BINGO!!", my2series[1])
        return map.turn

    # 2. 방어할 곳 확인1
    enemy = map.enemy()
    enemy2series = check2series(map.map, enemy)
    where = []
    if(enemy2series[0]):
        if(enemy2series[1][0] == "r"): # 막을 곳에 한 수 놓기
            where = [ int(enemy2series[1][1]), map.map[int(enemy2series[1][1])].index(".s") ]
        elif(enemy2series[1][0] == "c"):
            # print("col danger")
            col_pos = int(enemy2series[1][1])
            where = [col_pos] # row_pos 찾아서 넣을 것임.
            for row in range(0,3):
                if(map.map[row][col_pos] == ".s"):
                    where.insert(0, row)
                    break
        elif(enemy2series[1][0] == "s"): # cross check
            # print("cross danger")
            cross_num = int(enemy2series[1][1])
            # if crossList[0] = for L->R cross : s1 인 상황
            crossList = [[[0, 0], [1, 1], [2, 2]], [[0, 2], [1, 1], [2, 0]]]

            for idx in crossList[cross_num - 1]:
                if (map.map[idx[0]][idx[1]] == ".s"):
                    where = [idx[0], idx[1]]
                    break
        print("--> Dangerous!! Depend", where)
        map.update_map(where)
        return "continue"  # 아직 승부가 안났음

    # 3. min-max algorithm




    # 3. 한수를 두려고 했는데, 굳이 할 필요 없을 듯?
    # 아니야 그 한 수가 필요해
    return "I don't know"

def check2series(map_cur, check):
    # map_cur : 클래스가 아니라 오직 map list
    # check : check 하고 싶은 멤버

    # result is list 형태 [존재함, 어느 줄 빙고?] 예로, [1, "r1"] r1에서 빙고해서 이길 것임
    enemy = ""
    if (check == "X"):
        enemy = "O"
    else:
        enemy = "X"
    # row check
    for row in range(0, 3):  # 행 탐색 iterator ※ 중간까지만 확인해도 됨.
        for col in range(0, 2):  # 열 탐색 iterator
            if(map_cur[row][col][0] == check):
                if(map_cur[row][(col+1)%3][0] == check and map_cur[row][(col+2)%3][0] != enemy):
                    # 이미 Game Over 인 상태 (already 3 빙고) 끝 은 없는 걸로
                    return [1, "r" + str(row)]
                elif(map_cur[row][(col+2)%3][0] == check and map_cur[row][(col+1)%3][0] != enemy):
                    return [1, "r" + str(row)]

    # col check
    for row in range(0, 2):  # 행 탐색 iterator
        for col in range(0, 3):  # 열 탐색 iterator
            if(map_cur[row][col][0] == check):
                if(map_cur[(row+1)%3][col][0] == check and map_cur[(row+2)%3][col][0] != enemy):
                    # 이미 Game over 인 상태(already 3 빙고) 끝 은 없는 걸로
                    return [1, "c" + str(col)]
                elif(map_cur[(row+2)%3][col][0] == check and map_cur[(row+1)%3][col][0] != enemy):
                    return [1, "c" + str(col)]


    # cross check
    cross1 = [[0,0], [1,1]]  # check only 2, ignore [2,2]]
    cross2 = [[0,2], [1,1]]  # check only 2, ignore [2,0]]

    for idx in cross1:
        if (map_cur[idx[0]][idx[1]][0] == check) :
            if(map_cur[(idx[0]+1)%3][(idx[1]+1)%3][0] == check and map_cur[(idx[0]+2)%3][(idx[1]+2)%3][0] != enemy):
                return [1, "s1"]
            elif(map_cur[(idx[0]+2)%3][(idx[1]+2)%3][0] == check and map_cur[(idx[0]+1)%3][(idx[1]+1)%3][0] != enemy):
                return [1, "s1"]
    for idx in cross2:
        if (map_cur[idx[0]][idx[1]][0] == check) :
            if(map_cur[(idx[0]+1)%3][(idx[1]-1)%3][0] == check and map_cur[(idx[0]+2)%3][(idx[1]-2)%3][0] != enemy):
                return [1, "s2"]
            elif(map_cur[(idx[0]+2)%3][(idx[1]-2)%3][0] == check and map_cur[(idx[0]+1)%3][(idx[1]-1)%3][0] != enemy):
                return [1, "s2"]

    return [0, ""]  # 2 Series 없으면


# main 함수 호출
main()
