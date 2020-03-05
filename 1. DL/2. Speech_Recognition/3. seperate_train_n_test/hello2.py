'''
Oi, Oj : 오렌지의 위치 인덱스
Si, Sj : 멜론의 위치 인덱스
행렬(2차원리스트)의 i, j 를 의미함
'''


#pos에서 특정숫자(S)의 좌표를 찾는 함수
#숫자가 pos에 있으면 그 좌표(인덱스)를 반환
#없으면 -1 반환
def findIndex(pos,N,M,S):
    for i in range(N):
        for j in range(M):
            if pos[i][j]== str(S):
                return i,j
    return -1,-1

#오렌지와 멜론이 한 칸씩 이동할 때 이동한 후의 좌표를 찾는 함수
def findNextIndex(pos,Oi,Oj,Si,Sj,N,M):
    O = int(pos[Oi][Oj])            #현재의 O(오렌지)의 위치숫자
    S = int(pos[Si][Sj])            #현재의 S(멜론)의 위치숫자
    nextO = O+1                     #한 칸 이동한 위치
    nextS = S+1                     #한 칸 디오
    Oi, Oj = findIndex(pos,N,M,nextO)  #그때의 인덱스 찾기
    Si, Sj = findIndex(pos,N,M,nextS)  #그때의 인덱스 찾기
    return Oi,Oj,Si,Sj

#볼 수 있을 지 여부를 확인하는 함수
#가로, 세로, 대각선의 경우로 나누어 생각
#대각선 시 직선의 방정식을 이용함
def check(pos,N,M,Si,Sj,OrangeIndex):
    count = 0               #볼 수 있는 횟수
    Oi,Oj = findIndex(pos,N,M,1)             #오렌지가 처음으로 줄에 들어옴

    while Si != -1 or Sj != -1:     #멜론이 pos에서 나갈 때까지(인덱스가 -1일 때까지)반복
        #가로
        if Oi == Si:                #같은 행일 때
            if Oj<Sj:               #멜론이 더 오른쪽에 있을 시
                between = True      #멜론과 오렌지 사이에 누군가 있는지 여부를 확인
                                    #between = "True" 일 시 아무도 없음
                                    #False 일 시 누군가 있어 서로 볼 수 없음

                for j in range(Oj+1,Sj):            #사이에 누가 있는 지 확인
                    if pos[Oi][j]=="0":
                        between = True
                    else:
                        between = False
                if between == True:                 #사이에 아무도 없을 시 카운트 증가
                    count +=1
                    OrangeIndex.append(pos[Oi][Oj]) #그때의 오렌지의 위치숫자를 오렌지 인덱스에 추가(정답출력시 오렌지위치 출력위해)

            else:                   #오렌지가 더 오른쪽에 있을 시, 위와 동일한 방법
                for j in range(Sj+1,Oj):
                    if pos[Oi][j]=="0":
                        between = True
                    else:
                        between = False
                if between == True:
                    count +=1
                    OrangeIndex.append(pos[Oi][Oj])
            Oi, Oj, Si, Sj = findNextIndex(pos, Oi, Oj, Si, Sj, N, M)  #오렌지와 멜론을 한 칸 이동시킴



        #세로
        elif Oj==Sj:                 # 같은 열 일때
            if Oi<Si:                # 멜론이 더 아래 있을 때
                                     # 가로와 동일 한 방법으로 사이에 누가 있는 지 확인하고 아무도 없을 시 카운트증가
                                     # 그 후 한칸 이동
                between = True
                for i in range(Oi+1,Si):
                    if pos[i][Oj]=="0":
                        between = True
                    else:
                        between = False
                if between == True:
                    count +=1
                    OrangeIndex.append(pos[Oi][Oj])
            else:
                for i in range(Si+1,Oi):
                    if pos[i][Oj]=="0":
                        between = True
                    else:
                        between = False
                if between == True:
                    count +=1
                    OrangeIndex.append(pos[Oi][Oj])
            Oi, Oj, Si, Sj = findNextIndex(pos, Oi, Oj, Si, Sj, N, M)


        #대각선
        elif Si-Oi != 0 and Sj-Oj !=0:
            W = (Si - Oi) / (Sj - Oj)           # 멜론과 오렌지의 위치를 좌표로 생각하여 기울기를 구함
            B = Oi - W*Oj                       # 그때의 y절편
            line = lambda x: W * x + B          # 직선의 방정식
            if W>0:                             # 기울기가 양 일때(S가 O보다 더 오른쪽이 있을때)
                between = True
                for j in range(Oj+1,Sj):        # S와 O사이의 각각의 열(j)를 직선의 방정식에 대입해 그때의 값이 정수인지 확인
                    a = str(line(j))            # 직선에 대입해 얻은 값이 소숫점이하 1자리 실수형이라 그 값의 마지막이 0이면 정수라고 생각
                    if a[-1]=="0":              # 맨뒤의 값이 0이면 정수이므로, 정수이라면
                        if pos[int(line(j))][j] =="0":  # 또 그때 pos값이 0이라면 사이에 아무도 없다
                            between = True
                        else:
                            between = False
                if between == True:             # 사이에 아무도 없다면 카운트증가
                    count +=1
                    OrangeIndex.append(pos[Oi][Oj])

            else:                               # 기울기가 음 일때 (오렌지가 더 오른쪽에 있을 때) 위의 방법과 동일
                between = True
                for j in range(Sj+1, Oj):
                    a = str(line(j))
                    if a[-1]=="0":
                        if pos[int(line(j))][j] =="0":
                            between = True
                        else:
                            between = False
                if between==True:
                    count +=1
                    OrangeIndex.append(pos[Oi][Oj])
            Oi, Oj, Si, Sj = findNextIndex(pos, Oi, Oj, Si, Sj, N, M)  # 다음 칸으로 이동

        # else:           #위와 같은
        #     count += 1

    return count, OrangeIndex



if __name__ == "__main__":
    f = open("input.txt", "r")
    f2 = open("output.txt" ,"w")

    while 1:
        T = f.readline().rstrip()
        if T== "":
            break
        case = int(T[-1])
        N, M, S = map(int, f.readline().split())
        pos = []
        OrangeIndex =[]
        for i in range(N):
            pos.append(f.readline().split())
        Si, Sj = findIndex(pos,N,M,S)
        Answer, AnswerList = check(pos,N,M,Si,Sj,OrangeIndex)
        f2.write("Example ")
        f2.write(str(case))
        f2.write("\n")
        f2.write(str(Answer))
        f2.write("\n")
        for i in range(len(AnswerList)):
            f2.write(AnswerList[i])
            f2.write("\n")
        f2.write("\n")

    f.close()
    f2.close()