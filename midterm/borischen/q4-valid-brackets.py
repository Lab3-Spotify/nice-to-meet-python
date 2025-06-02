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

        