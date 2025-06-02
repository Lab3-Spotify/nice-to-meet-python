# input
lst = [1, 3, 7, 4, 5, 8]
N = 2

# main
target_list = sorted(lst)
Nth = int(N)
if Nth > len(target_list):
    print(f"小哥哥，沒有第{Nth}小的數字")
else:
    print(target_list[Nth-1])