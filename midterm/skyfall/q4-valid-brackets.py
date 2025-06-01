def bracket_reverse(bracket):
    if bracket == "]":
        return "["
    elif bracket == "}":
        return "{"
    elif bracket == ")":
        return "("
    return None

text = input("咿呀哈：")

if len(text) % 2 == 1:
    print("False")
    exit()

stack_list = []
for char in text:
    if char in "[{(":
        stack_list.append(char)
    elif char in "]})":
        if stack_list[-1] != bracket_reverse(char) :
            print("False")
            exit()
        else:
            stack_list.pop(-1)

if len(stack_list) == 0:
    print("True")
else:
    print("False")
