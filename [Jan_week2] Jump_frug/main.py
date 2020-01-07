# Manage with Class
class Map:  # 개구리 점프 stone 맵
    def __init__(self, case, numStone, stonesStr, maxDistance ):
        self.case = case  # number of case
        self.numStone = numStone

        self.stonesList = stonesStr.split(" ")  # string to list
        # remove '\n' at last element
        self.stonesList[numStone-1] = self.stonesList[numStone-1].replace("\n", "")

        self.MaxDistance = maxDistance

rfile = open("input.txt", mode="r")
wfile = open("output.txt", mode="wt", encoding="utf-8")  # 덮어씌우기 되겠지? oo

rlines = rfile.readlines()

totalCase = int(rlines[0])

for idx in range(0, totalCase):

    count = 0  # 점프 횟수
    jumpList = [0]

    #print("-----------")
    #print("Case #%d"%(idx + 1))

    # class 생성
    map = Map(idx+1, int(rlines[idx*3 + 1]), rlines[idx*3 + 2], int(rlines[idx*3 + 3]))
    #print("map.stonesList is ", map.stonesList)

    curPos = 0  # 0부터 시작 # 현재 밟고 있는 Stone 위치
    # MaxDistance 에서부터 한개씩 줄이면서 조사하자
    temp = curPos + map.MaxDistance
    #for i in range(1,10):
    #while(temp != 0 or str(curPos) != map.stonesList[len(map.stonesList)-1]):
    while(1):
        # Invariant Hypothesis
        ''' 
            curPos에서의 count가 curPos까지의 minimum 이다.
        '''
        if(str(curPos) == map.stonesList[len(map.stonesList)-1]):
            #print("끄읕")
            break
        if(str(temp) in map.stonesList):

            count = count + 1
            jumpList.append(temp)
            curPos = temp  # 그제서야 갱신해야되.
            #print("건널 수 있음", temp, jumpList)
            temp = temp + map.MaxDistance
            continue
        else:
            #print("temp--")
            temp = temp - 1
            if(temp <= curPos):  # 계속 줄어든 나머지, jumpList 이전으로 가버리면
                count = count - 1
                # jump 이전 위치로 갱신
                jumpList.pop()
                curPos = jumpList[-1] #마지막 요소
                if(curPos != 0):
                    temp = curPos + map.MaxDistance
                else:  # temp == 0
                    #print("No Solution. 건널 수 없음")
                    count = count-1 # make to -1
                    break

    txt = "\nCase #{}\n{}"
    wLines = txt.format(idx+1, count)  # 사실 count 는 len(jumpList)로도 가능
    print("[Case#%d]"%(idx+1), "output.txt 를 확인하세요....")
    wfile.writelines([wLines])

wfile.close()
