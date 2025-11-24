# coding=utf-8
# @Time    : 2025/11/24 9:15
# @Software: PyCharm

"""
计算50人生日不重复的概率
"""
numerator, denominator = 1, 1  # 分子分母
for i in range(50):
    # 第i+1个人的生日可选天数：365 - i
    numerator *= 365 - i
    denominator *= 365

result = numerator / denominator
print(f"50人生日完全不重复的概率：{result:.4f}（即 {result * 100:.2f}%）")
