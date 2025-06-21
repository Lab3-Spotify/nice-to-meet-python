x = 2
y = 8

result = False

# 第一類：x的特殊值
if x == 0:
    if y == 0.0:
        result = True
    else:
        result = False
elif x == 1:
    if y == 1.0:
        result = True
    else:
        result = False

elif x == -1:
    if y == 1.0 or y == -1.0:
        result = True
    else:
        result = False

# 第二類：y的特殊值
if not result:
    if y == 0:
        result = False
    elif y == 1.0:
        result = True

#第三類：一般情況
if not result:
    #  y > 0 時 
    if y > 0:
        # 正次方 
        current_power = float(x)
        
        while True:
            if current_power == y:
                result = True
                break
            if current_power > 0 and current_power > y:
                break
            
            if current_power == 0.0:
                break
            
            if abs(x) == 1: 
                break

            current_power *= x
            
        # 負次方
        if not result and x > 0:
            current_power = 1.0 / float(x)
            
            while True:
                if current_power == y:
                    result = True
                    break

                if current_power < y:
                    break
                
                if current_power == 0.0:
                    break
                
                current_power /= x

    #  y < 0 時
    elif y < 0:
        if x > 0:
            result = False
        else: # x為負數
            # 探索正奇數次方
            
            current_power = float(x)
            n = 1
            
            while True:
                if current_power == y:
                    result = True
                    break
                if abs(current_power) > abs(y) and current_power * y > 0:
                    break
                
                if current_power > 0:
                    break
                
                if current_power == 0.0:
                    break

                n += 2 # 跳到下一個奇數次方
                current_power = float(x) ** n 

            # 探索負奇數次方
            if not result:
                current_power = 1.0 / float(x) 
                n = -1
                
                while True:
                    if current_power == y:
                        result = True
                        break
                    if abs(current_power) < abs(y) and current_power * y > 0:
                        break
                    if current_power > 0:
                        break
                    if current_power == 0.0:
                        break
                    
                    n -= 2 # 跳到下一個負奇數次方
                    current_power = float(x) ** n 

# 輸出最終結果
print(result)

'''
# input
x = 2
y = 1

# main
result = False

if x != 0:
    if y == 1:
        result = True
    
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