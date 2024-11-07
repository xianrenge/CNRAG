# 相关函数



# 获取两列表的分组后最大值，按照l3的顺序给出分数
def group_and_max_by_order(l1, l2, l3):
    # 先获取每个id对应的最大值
    id_max_dict = {}
    for id_, val in zip(l1, l2):
        if id_ not in id_max_dict or val > id_max_dict[id_]:
            id_max_dict[id_] = val
    
    # 按照l3的顺序提取结果
    result = [id_max_dict[id_] for id_ in l3]
    return result

# 测试示例
l1 = [1, 1, 2, 2, 3, 3, 3]        # 原始id
l2 = [1.2, 2.3, 4.5, 1.8, 2.2, 3.1, 1.9]  # 分数
l3 = [2, 1, 3]                    # id的期望顺序

max_vals = group_and_max_by_order(l1, l2, l3)
print("按l3顺序的最大值:", max_vals)
