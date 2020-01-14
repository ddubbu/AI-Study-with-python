# rotate

import numpy as np #clockwise,anticlockwise rotation of matrix
n=int(input("Number of Rows of the Square Matrix:"))
arr=[]
print("Enter elements of Matrix:")
for i in range(n):
    l=list(map(int,input().split(",")))
    arr.append(l)
print("The given Matrix is:")
for i in range(n):
    for j in range(n):
        print(arr[i][j],end=" ")
    print()
m=np.array(arr,int)
s=input("Anticlockwise/Clockwise:")
d=input("Degrees:")
degrees={"90":1,"180":2,"270":3}
if(s=="Anticlockwise" or s=="ANTICLOCKWISE" ): #or s="aNTICLOCKWISE"
    m=np.rot90(m,degrees[d])
else:
    m=np.rot90(m,4-degrees[d])
print("The Matrix after rotation by the given degree.")
for i in range(n):
    for j in range(n):
        print(m[i][j],end=' ')
    print()