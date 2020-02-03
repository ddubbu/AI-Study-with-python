# It is problem of Euler's trail (열린 한붓 그리기)

# 0. 왜 그래프인가?
#   만약 "ab", "bc" 두 단어가 있다면, 각 글자를 vertax로 생각하고
#   첫글자와 끝글자 간의 연결관계가 edge 이다.
#   이때 방향성 있는 유향 그래프
#   [ex] 이와 같이 생각할 수 있다.
#           (a) -> (b) -> (c)
#   이때, 이 문제가 "열린 한붓그리기" 문제임이 확 와닿을 것이다.
#   붓을 떼지않고 모든 선을 지나는
#   즉, 모든 edge를 지나는 (있다면)순서 / (없다면) impossible 반환하는 문제인 것이다.

# 1. Set Graph with Matrix(= 2D List)
#   선택 이유: prefix와 suffix 간의 관계성을 연결해두고 싶었다.
#   Graph has only 26 nodes -> Matrix has 26*26 element
#   I use Matrix(=2D list) for Graph adjacent edges (숫자, word list)
#   row : start idx | col : end idx
#   [ex] words = ["ab", "acb", "bc", "cc"]를,  Matrix로 도식화
#          0 1 2 ... 25
#        0   2
#        1     1
#        2     1
#       ...
#        25
#   이때, G[0][1]["list"] = ["ab", "acb"] 와 같이 list 속성도 갖고 있다.

#   그리고, for indexing matrix use only number -> 알파벳 숫자 배정
#   -> dictionary 자료구조가 이럴 땐 편하지...
alp = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7, "i":8, "j":9,
        "k":10, "l":11, "m":12, "n":13, "o":14, "p":15, "q":16, "r":17, "s":18, "t":19,
        "u":20, "v":21, "w":22, "x":23, "y":24, "z":25}

# 2. DFS 탐색기법으로
#   - 모든 edge를 다 지나는 경우가 존재하는지 확인한다.
#   주요 탈출자는 47번째 조건으로, 이미 총 단어 개수만큼 word_chain 이 만들어졌으면 함수 반환
#   G(=Graph Matrix) 자체에서

def findTrail(G, start, num_word, word_chain):
    for finish in range(26):
        vertex = G[start][finish]

        while vertex["num"] > 0:
            vertex["num"] -= 1
            temp_pop = vertex["list"].pop()  # pop 을 잘해야지!
            word_chain.append(temp_pop)
            findTrail(G, finish, num_word, word_chain)
            if len(word_chain) == num_word:
                return word_chain
            else:
                vertex["num"] += 1
                vertex["list"].append(temp_pop)
                word_chain.pop()
                break

def main():
    # set read/write file variables
    rfile = open("input.txt", mode="r")
    wfile = open("output.txt", mode="wt", encoding="utf-8")

    # read each lines
    rlines = rfile.readlines()
    rlines.reverse()
    totalCase = int(rlines.pop())

    # iterative each Case
    for case in range(1, totalCase + 1):
        print("\n#case %d" % case)

        num_word = int(rlines.pop())
        # word_chain = []
        # initialize 2D adjacent matrix for graph
        G = [[{"num": 0, "list": []} for col in range(26)] for row in range(26)]

        # 1. read words and add to Graph
        for temp in range(num_word):
            word = rlines.pop()
            word = word.replace("\n", "")
            print(word)

            dic_temp = G[alp[word[0]]][alp[word[-1]]]
            dic_temp["num"] += 1
            dic_temp["list"].append(word)

        for s in range(26):  # 다 해보자..
            word_chain = []
            print("TRY #%d" %s)
            # G = copy_G
            result = findTrail(G, s, num_word, word_chain)
            if result and len(result) == num_word:
                print("정답:", result)
                wfile.write(str(result) + "\n")
                break
            else:
                wfile.write("IMPOSSIBLE\n")
                break
main()
print("끝")


# - print G edges
# print("   ", end="")
# alp_keys = list(alp.keys())
# for alpha in alp_keys:
#     print(alpha, " ", end="")
# print()  # 그냥 엔터 한번!
#
# for s in range(26):  # start, final idx
#     print(alp_keys[s], " ", end="")
#     # print(G[s])
#     for f in range(26):
#         print(G[s][f]["num"], " ", end="")
#         if f == 25:
#             print()

# - 시작점 쉽게 찾기
# 밑에는 무향 그래프 조건 인듯?
# # 시작점 in_degree +1 = out_degree
# s_vertex_candidate = []  # index(number) 가 요소임.
# for s in range(26):
#     # vertex "s" 에 대해서
#     in_degree = 0  # 들어오는 방향
#     out_degree = 0  # 나가는 방향
#     for f in range(26):
#         out_degree += G[s][f]["num"]
#         in_degree += G[f][s]["num"]
#     if in_degree + 1 == out_degree:
#         s_vertex_candidate.append(s)