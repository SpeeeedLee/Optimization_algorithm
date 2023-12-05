import random
import numpy as np



# 假设你有一个 True/False 列表
bool_list = [True, False, True, False, True]

# 你有一个包含数字的列表 x
x = [1, 2, 3, 4, 5]

# 使用列表推导式来根据 bool_list 中的值将 x 中对应位置的元素设置为 0 或保留原值
result = [0 if not condition else element for element, condition in zip(x, bool_list)]

print(result)
