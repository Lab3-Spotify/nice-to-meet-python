# 咿呀哈
lst = [2, 2, 3, 5, 6, 7, 9]

N = 4

lst_sort = sorted(list(set(lst)))
if N > len(lst_sort):
    print(f"沒有第{N}小的數字")
else:
    print(lst_sort[N-1])