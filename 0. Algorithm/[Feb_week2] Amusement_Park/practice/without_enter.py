import sys

def pushTo_wait_line(pos_new, wait_line):
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

        if x_min <= toCheck[1] and toCheck[1] <= x_max:
            if y_min <= toCheck[2] and toCheck[2] <= y_max:
                result.append(toCheck.copy())
    return result


# fp = sys.stdin
fp = open("test_input.txt", mode="r")
while True:
    pos_orange = [1, 1, 1]
    pos_melon = [0, 0, 0]
    wait_line = []

    rl = fp.readline()
    if not rl:
        break
    inform = rl.rstrip().split(' ')
    update_melon = int(inform[2])

    for row in range(1, int(inform[0]) + 1):
        temp = fp.readline().rstrip().split(' ')
        for col in range(int(inform[1])):
            pos = []
            if temp[col] != "0":
                pos = [int(temp[col]), row, col + 1]
                wait_line = pushTo_wait_line(pos.copy(), wait_line)  # sorting by ele[0]
            if int(temp[col]) == update_melon:
                pos_melon = [int(temp[col]), row, col + 1]
    a = 1
    b = 0
    how_many_run = wait_line[-1][0] - pos_melon[0] + 1
    answer = []
    for i in range(how_many_run):  # the number of total test
        canSee = 1
        check_list = isBetween(wait_line, pos_orange, pos_melon)
        for person in check_list:
            if (pos_orange[1] - pos_melon[1]) == 0:
                canSee = 0
                break

            else:
                a = (pos_orange[2] - pos_melon[2]) / (pos_orange[1] - pos_melon[1])
                b = pos_orange[2] - a * pos_orange[1]

                _y = a * person[1] + b
                if _y == person[2]:
                    canSee = 0
                    break

        if canSee:
            answer.append(pos_orange[0])

        if pos_melon[0] < wait_line[-1][0]:
            pos_orange = wait_line[pos_orange[0]]
            pos_melon = wait_line[pos_melon[0]]

    print(str(len(answer)))
    for ans in answer:
        print(str(ans))

    temp = fp.readline()
    #print()