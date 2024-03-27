# coding=utf-8
# @Time    : 2024/2/28 17:22
# @Software: PyCharm
from fractions import Fraction

"""
有三扇门，这三扇门的后面用一辆汽车和两只山羊，
在参赛者随机选择一扇门之后，主持人并不立刻打开这扇门，
主持人会从剩下的两扇门中打开一扇有山羊的那扇门，随后提供一次重新选择门的机会，
问：参赛者换门以后中奖的概率？
山羊数量为a，设中奖门数为b，主持人排除的门数量为c，则算式为：
a/(a+b) x b/(a+b-c-1)
"""


def three_door_question(sheep_num, prize_num, exclude_num):
    print(f"{sheep_num}羊，{prize_num}奖，会排除{exclude_num}个门")
    # 一开始选中山羊的概率
    sheep_chance = Fraction(sheep_num, (sheep_num + prize_num))
    # 主持人排除一定数量门后，奖品所占比例(排除当前选中的那个门)
    prize_chance = Fraction(prize_num, (sheep_num + prize_num - exclude_num - 1))
    return sheep_chance * prize_chance


print("换门之后的中奖概率：", three_door_question(2, 1, 1))
print("换门之后的中奖概率：", three_door_question(5, 1, 2))
