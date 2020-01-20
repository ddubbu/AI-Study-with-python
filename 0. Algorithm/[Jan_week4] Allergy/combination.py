
# 문제의 코드

def combination(m, k):
    # 0~m-1 까지의 숫자 중에서 k개를 추출할 수 있는 경우의 수
    list_num = list(range(0, m))
    print("list is", list_num)

    result = []
    print("m: %d, k: %d" % (m, k))
    def generate(chosen):

        if len(chosen) == k:
            print("chosen is", chosen)
            print("before result :", result)
            # result.append(chosen) # 대박, 이것은 주소를 넘기는 것이여! 복사본을 넘기자!
            copy = chosen.copy()
            result.append(copy)
            print("after result :", result)
            return
        # one line 조건문
        start = list_num.index(chosen[-1]) + 1 if chosen else 0
        for nxt in range(start, len(list_num)):
            chosen.append(list_num[nxt])
            generate(chosen)
            chosen.pop()
    generate([])

    return result

combination(3, 2)