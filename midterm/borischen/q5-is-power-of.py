# input
x = -2
y = -0.125


# main
if y>0 and x<y and y!=1:
    outcome = 0
    temp = x
    while outcome < y:
        temp = temp*x
        outcome = abs(temp)
    
    if temp == y:
        print(True)
    else:
        print(False)

elif y == 1:
    print(True)
elif y>0 and abs(x)>y and y!=1:
    outcome = 0
    temp = (1/x)
    while outcome < y:
        temp = temp*(1/x)
        outcome = abs(temp)
    
    if temp == y:
        print(True)
    else:
        print(False)

elif y<0 and x>y and y!=1:
    outcome = 0
    temp = x
    while outcome < abs(y):
        temp = temp*x
        outcome = abs(temp)
    
    if temp == y:
        print(True)
    else:
        print(False)
elif y<0 and x<y and y!=1:
    outcome = abs(x)
    temp = (1/x)
    while outcome > abs(y):
        temp = temp*(1/x)
        outcome = abs(temp)
    
    if temp == y:
        print(True)
    else:
        print(False)
elif x == 1:
    if y != 1:
        print(False)
    else:
        print(True)
        
elif x == -1:
    if y == 1 or y == -1:
        print(True)
    else:
        print(False)