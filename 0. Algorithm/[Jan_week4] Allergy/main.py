
class table:
    def __init__(self, case, rlines):

        self.case = case
        self.table = []  # col = friends idx, row = foods idx
                    # ele = (1 : 먹을 수 있음), (0 : 먹을 수 없음)

        num_ff = rlines.pop().split(" ")
        self.num_friends = int(num_ff[0])  # column
        self.num_foods = int(num_ff[1])  # row

        self.list_friends = rlines.pop().split(" ")
        self.list_friends[-1] = self.list_friends[-1].replace("\n", "")  # 마지막 요소 엔터 없애기

        for r_idx in range(0, self.num_foods):
            # 각 음식별로 no_allergy 리스트 업데이트하기
            # 각 친구별로 순회해서 먹을수 있으면 1, 없다면 0으로 값 저장
            vector_row = []
            list_no_allergy = rlines.pop().split(" ")
            list_no_allergy[-1] = list_no_allergy[-1].replace('\n', "")
            del list_no_allergy[0]
            for friends in self.list_friends:
                if friends in list_no_allergy:
                    vector_row.append(1)
                else:
                    vector_row.append(0)

            # r_idx 번째(음식)에 대해 생성한 vector_row table에 업데이트 하기
            self.table.append(vector_row)

    def drawTable(self):
        print("\n#Case", self.case)
        for row in range(0, self.num_foods):
            print(self.table[row])

    def indexList_Friends(self):
        return list(range(0, self.num_friends))

def combinations(iterable, r):
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = list(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield list(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield list(pool[i] for i in indices)

def main():
    # set read/write file variables
    rfile = open("input.txt", mode="r")
    wfile = open("output.txt", mode="wt", encoding="utf-8")

    # read each lines
    rlines = rfile.readlines()
    rlines.reverse()
    '''
        the first line has (total) the number of case
        계속 rlines를 인덱스로 접근하다가, 
        reverse 한 후 pop메소드로 뒤에서부터 꺼내기로함! ^^
        왜 unshift 메소드가 없는거지 :-( 
    '''
    totalCase = int(rlines.pop())
    # iterative each Case

    for case in range(1, totalCase + 1):

        # 1. make table
        t = table(case, rlines)
        num_minFoods = t.num_foods

        # 2. mCk 개씩 food 를 선택해서 모든 친구를 수용할 수 있는 최소 k 찾기
        # m : t.num_foods, k : iterator 1 ~ t.num_foods
        # 단, itertools 모듈 from permutations 쓰지 말고!
        t.drawTable()
        isbreak = 0
        for k in range(1, t.num_foods + 1):
            for checklist_foods in combinations(range(0,t.num_foods), k):
                remainlist_friends = t.indexList_Friends()

                '''
                mCk로 생성한 checklist_foods를 iterative list로 삼는다.
                현재 음식을 먹을 수 있는 친구는 
                리스트(remainlist_friends) 에서 제외
                    .... ing ...
                해당 checklist_food == empty 이면
                현재 checklist_foods 가 가장 최소 요구 음식
                '''
                for food in checklist_foods: #food : row idx, 숫자
                    list_remove = []
                    for friend in remainlist_friends: #friend : col idx, 숫자
                        isNoAllergy = t.table[food][friend] #(1: 먹음, 0: 못먹음)
                        if isNoAllergy:
                            # remainlist_friends.remove(friend) # 여기서 삭제하면 그 다음 idx로 안넘어가네
                            list_remove.append(friend)

                    for remove in list_remove:
                        remainlist_friends.remove(remove)

                if len(remainlist_friends) == 0:
                    num_minFoods = k  # len(checklist_foods)
                    isbreak = 1
                    break  # stop find mCk

            if isbreak :  # 번거롭고만
                break

        wfile.write(str(num_minFoods) + "\n")



main()