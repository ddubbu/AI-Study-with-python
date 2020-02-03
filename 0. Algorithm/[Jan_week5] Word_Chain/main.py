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
#   I use Matrix(=2D list) for Graph adjacent edges (= word list)
#   row : start idx | col : end idx
#   [ex] words = ["ab", "acb", "bc", "cc"]를,  Matrix로 도식화
#          0  1  2   ... 25
#        0   2개
#        1      1개
#        2      1개
#       ...
#        25
#   이때, G[0][1] = ["ab", "acb"] 와 같이 list 속성을 갖고 있다.

#   그리고, for indexing matrix use only number -> 알파벳 숫자 배정 -> 이점은 dictionary가 더 유용한듯

alp = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7, "i":8, "j":9,
        "k":10, "l":11, "m":12, "n":13, "o":14, "p":15, "q":16, "r":17, "s":18, "t":19,
        "u":20, "v":21, "w":22, "x":23, "y":24, "z":25}

# 2. DFS 탐색기법으로
#   - 모든 edge를 다 지나는 경우가 존재하는지 확인한다.
#   주요 탈출자는 51번째 조건으로, 이미 총 단어 개수만큼 word_chain 이 만들어졌으면 word_cahin 값 반환
#
#   G(=Graph Matrix) 자체에서 꺼내서 word_chain에 넣었으므로,
#   solution route가 아니면 else문(53-56번째 줄)에서처럼,
#   다시 Graph에 넣고 word_chain에서도 다시 꺼내기(pop())
#
#   Matrix의 또다른 단점, 넘어갈 다음(finish) vertex 지점을 다 순회해야한다.

def findTrail(G, start, num_word, word_chain):

    for finish in range(26):
        vertex = G[start][finish]
        while len(vertex) > 0:
            temp_pop = vertex.pop()  # pop 을 잘해야지!
            word_chain.append(temp_pop)
            findTrail(G, finish, num_word, word_chain)
            if len(word_chain) == num_word:
                return word_chain
            else:
                vertex.append(temp_pop)
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
        # initialize 2D adjacent matrix for graph
        G = [[ [] for col in range(26)] for row in range(26)]

        # 1. read words and add to Graph
        for temp in range(num_word):
            word = rlines.pop()
            word = word.replace("\n", "")
            print(word)

            dic_temp = G[alp[word[0]]][alp[word[-1]]]
            dic_temp.append(word)

        # 2. DFS, 시작점을 달리해보면서
        is_There = 0  # 답 출력 여부 확인
        for start in range(26):  # ★ 시작점이 될 수 있는 오일러 트레일 조건을 다시 찾아보자
            word_chain = []
            print("|TRY|시작점 : 알파벳 %d번째 " %start)
            result = findTrail(G, start, num_word, word_chain)
            print("result: ", result)
            if result and len(result) == num_word:
                print("정답:", result)
                wfile.write(' '.join(result) + "\n")
                is_There = 1
                break
            else:
                continue

        if is_There == 0:
            wfile.write("IMPOSSIBLE\n")

main()
print("끝")