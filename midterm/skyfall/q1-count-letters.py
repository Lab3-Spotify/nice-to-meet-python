# 咿呀哈
counts = {}

texts = input("咿呀哈：")

for char in texts:
    if char in counts:
        counts[char] += 1
    else:
        counts[char] = 1

name_order = "please solve the conflict and remove this line"
value_order = sorted(name_order, key=lambda x: x[1], reverse=True)
for character, count in value_order:
    print(f"{character} {count}")