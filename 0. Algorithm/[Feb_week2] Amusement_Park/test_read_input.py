rfile = open("test_input.txt", mode="r")

case = 0
if '1' == rfile.readline().rstrip().split(' ')[0]:
    case = 1
else:
    case = -1

while case != -1:
    inform = rfile.readline().rstrip().split(' ')
    for row in range(1, int(inform[0]) + 1):
        print(rfile.readline().rstrip())

    if rfile.readline() == None or rfile.readline().split(' ')[0] != "Example":
        case = -1
    else:
        case += case
    print()
