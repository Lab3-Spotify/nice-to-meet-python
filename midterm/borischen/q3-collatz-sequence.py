input_1 = 20
input_2 = 30

def cycle_length(n):
    if n == 1:
        return 1
    elif n % 2 == 0:
        return 1 + cycle_length(n // 2)
    else:
        return 1 + cycle_length(3*n + 1)
        
biggest = 0
biggest_cycle_length = 0
for i in range(input_1, input_2+1):
    if cycle_length(i) > biggest_cycle_length:
        biggest_cycle_length = cycle_length(i)
        biggest = i

print(biggest)