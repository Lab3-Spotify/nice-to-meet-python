# 咿呀哈
a = int(input("咿呀哈："))
b = int(input("咿呀哈哈："))

max_length = 0
max_length_number = 0
for num in range(a, b+1):
    length_count = 0
    number = num  # 保存原始數字以便於輸出
    while num != 1:
        if num % 2 == 0:
            num //= 2
        else:
            num = num * 3 + 1
        length_count += 1
    if length_count > max_length:
        max_length = length_count
        max_length_number = number

print(max_length_number)