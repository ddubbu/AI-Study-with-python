This is program for Assign1, " Jump Frug "
Find minimum(optimal) steps for crossing the stone bridge.

1. Set form of input file(input.txt) !
[ex]
    2 # Total Number of cases
    8 # (1st Case) Total Number of stones
    1 2 5 7 9 10 12 15 # Series of stones
    4 # Maximum step
    8 # (2nd Case) ...
    1 2 5 7 9 10 12 15
    2

2. Executing main.py, output.txt will be made.
    Result is minimum(optimal) step count.
    If there isn't optimal value, it will be (-1)
[ex]
    Case #1
    5
    Case #2
    -1

3. What is different from version 1 ?
    - I removed Class Data Structure.
    (But I don't know why it needs still.. I will ask the reason later)

    - and modify source to module/function as JumpCount
    But I don't set arguments. anyway just call it with this code
    [ex]
        from Jump_Frug import JumpCount
        JumpCount()

