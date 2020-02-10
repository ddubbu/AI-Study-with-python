def pushTo_wait_line(pos_new, wait_line):  # 정렬하기 위함
    idx_insert = 0
    if len(wait_line) != 0:
        for i in range(0, len(wait_line)):
            if pos_new[0] > wait_line[i][0]:
                idx_insert = i + 1
                pass
            else:
                break

    wait_line.insert(idx_insert, pos_new)
    return wait_line


def isBetween(wait_line, orange, melon):
    result = []
    x_min = min(orange[1], melon[1])
    x_max = max(orange[1], melon[1])
    y_min = min(orange[2], melon[2])
    y_max = max(orange[2], melon[2])

    for toCheck in wait_line:
        if toCheck == orange or toCheck == melon:
            continue

        if x_min <= toCheck[1] <= x_max:  # 파이참 제공 문법
            if y_min <= toCheck[2] <= y_max:
                result.append(toCheck.copy())

    return result


def main():
    # set read/write file variables
    rfile = open("input.txt", mode="r")
    wfile = open("output.txt", mode="wt", encoding="utf-8")

    total_case = int(rfile.readline().rstrip())

    for case in range(total_case):
        # initialize
        pos_orange = [1, 1, 1]  # num_line, idx_row, idx_col
        pos_melon = [0, 0, 0]  # I don't know not yet
        wait_line = []

        rfile.readline()  # 그냥 위에 엔터
        print("\n--------\n", rfile.readline().rstrip())  # 그냥 "Example N"
        inform = rfile.readline().rstrip().split(' ')
        update_melon = int(inform[2])  # later, i will update with position

        # 1. make wait_line map with [num_line, x, y]
        for row in range(1, int(inform[0]) + 1):
            temp = rfile.readline().rstrip().split(' ')
            for col in range(int(inform[1])):  # 얘는 0부터 커진다는 점 조심하고
                pos = []
                if temp[col] != "0":
                    pos = [int(temp[col]), row, col+1]
                    wait_line = pushTo_wait_line(pos.copy(), wait_line)  # 0번째 요소값에 따라 알아서 정렬되어 넣기
                if int(temp[col]) == update_melon:
                    pos_melon = [int(temp[col]), row, col+1]
        print("wait_line is", wait_line)

        # 2. make equation and check only between people

        a = 1
        b = 0
        how_many_run = wait_line[-1][0] - pos_melon[0] + 1
        answer = []
        for i in range(how_many_run):
            print("----------")
            print("now orange:", pos_orange, " melon:", pos_melon)
            canSee = 1

            # 범위 안에 있는 사람들만 체크하기
            check_list = isBetween(wait_line, pos_orange, pos_melon)
            for person in check_list:
                # 1) equation 방법으로 정의될 수 없는 상황 예외처리 : 기울기가 무한대
                if (pos_orange[1] - pos_melon[1]) == 0:  # x 좌표값만 비교해서 사이에 있는 값이 있는지 체크
                    canSee = 0
                    print("[Can't See] case1 by", person)
                    break

                else:  # 2) equation 방법으로
                    # initialize
                    a = (pos_orange[2] - pos_melon[2]) / (pos_orange[1] - pos_melon[1])
                    b = pos_orange[2] - a * pos_orange[1]

                    _y = a*person[1] + b
                    if _y == person[2]:  # 직선 위에 있는지
                        canSee = 0
                        print("[Can't See] case2 by", person)
                        break  # 볼 수 없음.

            if canSee:
                answer.append(pos_orange[0])

            # (마지막 요소가 아니면) move to next position
            if pos_melon[0] < wait_line[-1][0]:
                # different between wait_line idx + 1 = 현재 위치
                pos_orange = wait_line[pos_orange[0]]  # 그러므로 그 값을 넘기면 알아서 업데이트 됨
                pos_melon = wait_line[pos_melon[0]]

        # end of process
        wfile.write("Example " + str(case + 1) + "\n")
        wfile.write(str(len(answer)) + "\n")
        for ans in answer:
            wfile.write(str(ans) + "\n")

        wfile.write("\n")

main()



