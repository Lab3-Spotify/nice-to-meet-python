# input
input_bracket = '({})'

left_bracket = ['(', '[', '{']
bracket_dict = {'(': ')', '[': ']', '{': '}'}

check_list = []
is_valid = True
top = -1

for s in input_bracket:
    if s in left_bracket:
        check_list.append(s)
        top = top + 1
    else:
        if top == -1:
            is_valid = False
            break
        if bracket_dict[check_list[top]] != s:
            is_valid = False
            break
        else:
            last_item = check_list.pop() 
            top = top - 1 # 改成不會馬上print，全部檢查完再print

if top != -1:
    is_valid = False

print(is_valid)

'''
原版
# input
input_bracket = '({})'

left_bracket = ['(', '[', '{']
bracket_dict = {'(': ')', '[': ']', '{': '}'}

check_list = []
top = -1

for s in input_bracket:
    if s in left_bracket:
        check_list.append(s)
        top = top + 1
    else:
        if bracket_dict[check_list[top]] != s:
            print(False)
        else:
            last_item = check_list.pop() 
            top = top - 1
            if top == -1:
                print(True)
'''
        