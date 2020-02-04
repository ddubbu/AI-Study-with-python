### 1. make wait_line map with [num_line, x, y]
이때, 좌표 x,y 는
(1,1)을 기준으로 좌표값을 설정한다.
x방향: +1(남), -1(북)
y방향: +1(동), -1(서)

(1,1) ㅡ ㅡ ㅡ y (col)
|
|
|
x
(row)

* Example
3 4 6
1 2 3 0
0 5 4 0
0 6 7 8

wait_line = [[1, 1, 1], [2, 1, 2], [3, 1, 3], [4, 2, 3], [5, 2, 2], [6, 3, 2], [7, 3, 3], [8, 3, 4]]

* 사용한 함수
pushTo_wait_line(pos_new, wait_line)

우선, readline()으로 한 줄씩 읽고 split한 다음, 값이 0이 아니라면,
[num_line, x, y] 배열을 만들어서 wait_line에
앞에서부터 num_line 기준으로 "insert sort" 한다.

파이썬은 다행히 list.insert(idx_insert, ele) 함수가 있어서
밀어내지 않고 자리만 지정해주면 된다.

* wait_line sort 하는 이유
나중에, orange, melon 위치 업데이트를 쉽게 하기 위해
단순히 배열 인덱스를 한칸만 올리면 되니깐

### 2. make equation and check only between people

1) make equation with 2점 (melon, orange)
y = ax + b, a:기울기, b:y절편

2) check_list = isBetween(wait_line, pos_orange, pos_melon)
: orange, melon 사이에 있는 사람들만 가져오기
※ 이때, 무조건 pos_orange < pos_melon이라고 생각했는데
상위 위치(x좌표가 출구랑 가까운) 가 orange가 될 수 있다.
그래서, x_min, x_max 와 같은 변수를 만들어서 비교함.

3) check_list에 있는 사람 중 1) eqution을 만족하는 점(사람)이 있다면
orange can't see melon

4) 예외사항
(1) a =  무한대(y축과 평행한) 인 equqtion 정의 불가
