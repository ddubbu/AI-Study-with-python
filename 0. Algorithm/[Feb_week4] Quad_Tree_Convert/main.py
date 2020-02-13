def init_node(value):
    node = [value, [None, None, None, None]]
    return node


def make_tree(ptr, string, idx):  # recursion
    if idx < len(string):
        value = string[idx]

        # 조심 : ptr = init_node(value) 이러면, T root 주소값 초기화된다.
        ptr[0] = value
        idx += 1
        if value == "x":
            for i in range(4):
                # 자식 노드로 넘어갈때, None이 아닌 빈칸 노드로 넘어가도록!
                ptr[1][i] = init_node(value)
                idx = make_tree(ptr[1][i], string, idx)  # recursive
    return idx


# DFS, stack(대신, 4번째 child 부터 스택에 넣기)
def print_tree(ptr, stack):
    if len(stack) == 0 and ~ptr[0]:
        stack.append(ptr)  # 포인터를 넣기

    while len(stack) != 0:  # 스택이 비지 않을 때까지 돌리기
        pop = stack.pop()
        if ~pop:
            print(pop[0], end="")
        if pop[0] == "x":  # 4번째 아이부터 넣으면, 1번째 아이부터 출력됨.
            # 정상 읽는 순서 : 1->2->3->4
            stack.append(pop[1][3])
            stack.append(pop[1][2])
            stack.append(pop[1][1])
            stack.append(pop[1][0])

def print_convert_tree(wfile, ptr, stack):
    if len(stack) == 0 and ~ptr[0]:
        stack.append(ptr)  # 포인터를 넣기
    while len(stack) != 0:  # 스택이 비지 않을 때까지 돌리기
        pop = stack.pop()
        if ~pop:
            wfile.write(pop[0])
            # print(pop[0], end="")
        if pop[0] == "x":
            # 정상 읽는 순서(idx): 0(왼쪽위)->1(오른쪽위)->2(왼쪽아래)->3(오른쪽아래)
            # 이미지 반대로 읽기 : 2->3->0->1 (나중에 읽는 아이를 스택에 먼저 넣기)
            stack.append(pop[1][1])
            stack.append(pop[1][0])
            stack.append(pop[1][3])
            stack.append(pop[1][2])


if __name__ == "__main__":
    # set read/write file variables
    rfile = open("input.txt", mode="r")
    wfile = open("output.txt", mode="wt", encoding="utf-8")

    total_case = int(rfile.readline())
    for case in range(1, total_case + 1):
        # print("#", case)
        string = rfile.readline().rstrip()
        T = init_node(None)
        make_tree(T, string, 0)
        # print_tree(T, [])
        print_convert_tree(wfile, T, [])
        wfile.write("\n")



