def set_link(map, N, inform_connecting, inform_shortest, not_linked_cores, idx,
             direc):  # direc : 동(E), 서(W), 남(S), 북(N)
    # inform_connecting = [num_linked_core, num_linked_line]
    # inform_shortest = [max_linked_core, short_linked_line]

    # start from position of core

    if idx >= len(not_linked_cores):
        return inform_shortest

    what_core = not_linked_cores[idx]
    pos_r = what_core[0]
    pos_c = what_core[1]

    # move direc
    move_r = 0
    move_c = 0

    if direc == "E":
        move_c = 1
    elif direc == "W":
        move_c = -1
    elif direc == "S":
        move_r = 1
    elif direc == "N":
        move_r = -1

    # 우선 전선을 놓을 수 있는지 체크하기
    isOk = True
    while isOk:
        # 자리 갱신하고
        pos_r += move_r
        pos_c += move_c
        if (0 <= pos_r < N) and (0 <= pos_c < N):
            value = map[pos_r][pos_c]
            if value == "1" or value == "_":
                isOk = False
            else:
                pass
        else:
            break

    # temp_inform_shortest = inform_shortest.copy()
    if isOk:
        inform_connecting[0] += 1
        pos_r = what_core[0]
        pos_c = what_core[1]
        while 1:
            # 자리 갱신하고
            pos_r += move_r
            pos_c += move_c
            if (0 <= pos_r < N) and (0 <= pos_c < N):
                map[pos_r][pos_c] = "_"
                inform_connecting[1] += 1
            else:
                break

        if inform_connecting[0] == inform_shortest[0]:  # 연결된 코어 수가 같을 때
            if inform_connecting[1] < inform_shortest[1]:  # line 수가 더 적으면 값 업데이트
                inform_shortest = inform_connecting.copy()

        elif inform_connecting[0] > inform_shortest[0]:  # 연결된 코어 수가 더 많으면
            inform_shortest = inform_connecting.copy()  # 무조건 업데이트

    direction = ["E", "W", "S", "N"]
    for direc2 in direction:
        inform_shortest = set_link(map, N, inform_connecting, inform_shortest, not_linked_cores, idx + 1, direc2)

    # DFS 하고 제자리 해보자 : 길 삭제
    if isOk:
        inform_connecting[0] -= 1
        pos_r = what_core[0]
        pos_c = what_core[1]
        while 1:
            # 자리 갱신하고
            pos_r += move_r
            pos_c += move_c
            if (0 <= pos_r < N) and (0 <= pos_c < N):
                map[pos_r][pos_c] = "0"  # 길 없애기
                inform_connecting[1] -= 1
            else:
                break

        # inform_shortest = temp_inform_shortest

    return inform_shortest


if __name__ == "__main__":

    # 1. read input file
    # set read/write file variables
    # rfile = open("input.txt", mode="r")
    # wfile = open("output.txt", mode="wt", encoding="utf-8")

    total_case = int(input().rstrip())
    for case in range(1, total_case + 1):
        N = int(input().rstrip())
        map = []

        for i in range(N):
            map.append(input().rstrip().split(" "))  # 다 string 임을 잊지 말고!

        # print(map)

        # 2. read core spec
        num_core = 0
        num_linked_core = 0
        not_linked_cores = []
        shortest_line = N * N
        for r in range(N):
            for c in range(N):
                if map[r][c] == "1":
                    num_core += 1
                    if r == 0 or c == 0:
                        num_linked_core += 1  # 이미 연결되었으니, 개수 늘리기
                    else:
                        not_linked_cores.append([r, c])

        # 3. DFS 재귀에게 맡겨라
        # set_link(map, N, num_linked_core, not_linked_cores[0], "E")
        # for i in range(N):
        #     print(map[i])

        inform_linked = [num_linked_core, 0]
        inform_shortest = [num_linked_core, N * N]  # max value
        direction = ["E", "W", "S", "N"]

        for direc in direction:
            inform_shortest = set_link(map, N, inform_linked, inform_shortest, not_linked_cores, 0, direc)

        print("#%s" % case, end=" ")
        print(inform_shortest)

