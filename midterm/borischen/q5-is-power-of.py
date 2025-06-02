# input
x = 4
y = 1

# main
result = False

if x != 0:
    if y == 1:
        print(True)
    # 正整數次方
    temp = x
    while abs(temp) <= abs(y) or (x < 0 and y < 0):
        if abs(temp - y) < 1e-9:
            result = True
            break
        temp *= x
    
    # 負整數次方
    if not result:
        try:
            temp = 1 / x
            while abs(temp) >= abs(y):
                if abs(temp - y) < 1e-9:
                    result = True
                    break
                temp /= x
        except ZeroDivisionError:
            pass

print(result)

'''
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
'''