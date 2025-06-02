# input
lst = [1, 3, 7, 4, 5, 8]
N = 2

# main
target_list = sorted(set(lst)) # 補上一個set讓去重
if N > len(target_list):
    print(f"小哥哥，沒有第{N}小的數字")
else:
    print(target_list[N-1])