
def JumpCount():
    # set read/write file variables
    rfile = open("input.txt", mode="r")
    wfile = open("output.txt", mode="wt", encoding="utf-8")

    # read each lines
    rlines = rfile.readlines()

    # the first line has (total) the number of case
    totalCase = int(rlines[0])

    # iterative each Case
    for idx in range(0, totalCase):
        count = 0  # Count jump
        jumpList = [0] # Jump List

        # print("-----------")
        # print("Case #%d"%(idx + 1))

        # update value
        case = idx+1  # number of case
        numStone = int(rlines[idx*3 + 1])
        stonesList = rlines[idx*3 + 2].split(" ")  # string to list
        # remove '\n' at last element
        stonesList[numStone - 1] = stonesList[numStone - 1].replace("\n", "")
        MaxDistance = int(rlines[idx*3 + 3])

        curPos = 0  # 0부터 시작 # 현재 밟고 있는 Stone 위치
        # MaxDistance 만큼 뛰어서 stone 위치할때까지 한개씩 줄이면서 조사하자
        temp = curPos + MaxDistance
        while(1):
            # Invariant Hypothesis
            ''' 
                curPos에서의 count가 curPos까지의 minimum 이다.
            '''
            if(str(curPos) == stonesList[len(stonesList)-1]):
                # print("끄읕")
                break
            if(str(temp) in stonesList):

                count = count + 1
                jumpList.append(temp)
                curPos = temp  # 그제서야 갱신해야되.
                # print("건널 수 있음", temp, jumpList)
                temp = temp + MaxDistance
                continue
            else:
                # print("temp--")
                temp = temp - 1
                if(temp <= curPos):  # 계속 줄어든 나머지, jumpList 이전으로 가버리면
                    count = count - 1
                    # jump 이전 위치로 갱신
                    jumpList.pop()
                    curPos = jumpList[-1] #마지막 요소
                    if(curPos != 0):
                        temp = curPos + MaxDistance
                    else:  # temp == 0
                        # print("No Solution. 건널 수 없음")
                        count = count - 1  # make to -1
                        break

        txt = "\nCase #{}\n{}\n"
        wLines = txt.format(idx+1, count)  # 사실 count 는 len(jumpList)로도 가능
        wfile.writelines([wLines])

    wfile.close()

