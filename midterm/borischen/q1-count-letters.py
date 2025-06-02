# input
input_str = "bbaaccc"

# main
input = str(input_str)
target = sorted(list(set(input))) # 以set找出要做計算的target並轉成list，再對這個list進行sort先進行字母排序
    
count_list = []
for t in target:
    count = 0
    for c in input:
        if c == t:
            count = count + 1
    count_list.append(count) # 直接依據字母排序後的target算count
    
keys = target
count_dict = {k: v for k, v in zip(keys, count_list)} # 把key跟value對起來
    
sorted_key = sorted(list(count_dict.keys()),key=lambda k: count_dict[k], reverse=True) # 判斷dict中value的值，將根據count排序過後的key存在sorted_key裡 (不確定這樣會不會影響到字母順序，從測資上看是沒有)
    
sorted_dict = {k: count_dict[k] for k in sorted_key} # 把key跟value對起來
    
for key in sorted_dict:
    print(f"{key} {sorted_dict[key]}")