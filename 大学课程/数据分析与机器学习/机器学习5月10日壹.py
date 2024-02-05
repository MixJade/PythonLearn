import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

attribute = {
    "色泽": ['青绿', '乌黑', '浅白'],
    "根蒂": ['蜷缩', '稍蜷', '硬挺'],
    "敲声": ['浊响', '沉闷', '清脆'],
    "纹理": ['清晰', '稍糊', '模糊'],
    "脐部": ['凹陷', '稍凹', '平坦'],
    "触感": ['硬滑', '软粘'],
    # "密度":[],
    # "含糖率":[],
}

# 用来正常显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']
# 用来正常显示负号
plt.rcParams['axes.unicode_minus'] = False
labels = ['是', '否']


def loaddata(dir01):
    data01 = pd.read_excel(dir01)
    return data01


def entropy(d01):
    count = d01.shape[0]
    ent = 0.0
    temp = d01['好瓜'].value_counts()  # 获取剩余的类别数量
    for i in temp:
        ent -= i / count * np.log2(i / count)
    return round(ent, 3)


def cal_gain(d02, ent, a02):
    """
    D:剩余的样本集
    Ent：对应的信息熵
    A：剩余的属性集合
    """
    # print("gain:",A)
    gain = []
    count = d02.shape[0]
    for i in a02:
        temp = 0
        for j in attribute[i]:
            temp += d02[(d02[i] == j)].shape[0] / count * entropy(d02[(d02[i] == j)])
        # print(temp)
        gain.append(round(ent - temp, 3))
        # print(i,round(Ent-temp,3))
    return np.array(gain)


def same_value(d03, a03):
    for key in a03:
        if key in attribute and len(d03[key].value_counts()) > 1:
            return False
    return True


# 叶节点选择其类别为D中样本最多的类
def choose_largest_example(D):
    count = D['好瓜'].value_counts()
    return '是' if count['是'] >= count['否'] else '否'


def choose_best_attribute(D, A):
    Ent = entropy(D)
    gain = cal_gain(D, Ent, A)
    return A[gain.argmax()]


# A:剩余的属性集
def tree_generate(D, A):
    Count = D['好瓜'].value_counts()
    if len(Count) == 1:  # 情况一，如果样本都属于一个类别
        return D['好瓜'].values[0]

    if len(A) == 0 or same_value(D, A):  # 情况二：如果样本为空或者样本的所有属性取值相同，则取类别较多的为分类标准
        return choose_largest_example(D)

    node = {}
    best_attr = choose_best_attribute(D, A)  # 情况三：选择一个最佳属性作为分类节点
    D_size = D.shape[0]
    # 最优划分属性为离散属性时
    for value in attribute[best_attr]:  # 对最佳属性当中的每个属性值进行分析
        Dv = D[D[best_attr] == value]
        if Dv.shape[0] == 0:
            node[value] = choose_largest_example(D)
        else:
            new_A = [key for key in A if key != best_attr]
            node[value] = tree_generate(Dv, new_A)
    return {best_attr: node}


# 决策树可视化
def drawtree(tree, coordinate, interval):
    """
    tree：决策树
    coordinate: 当前节点的坐标
    interval：分支节点间的间隔
    """
    now_A = list(tree.keys())[0]
    plt.text(coordinate[0], coordinate[1], now_A, size=15,
             ha="center", va="center",
             bbox=dict(boxstyle="round",
                       ec=(0.5, 0.8, 0.1),
                       fc=(0.5, 0.8, 0.1),
                       )
             )
    split_num = len(tree[now_A].values())
    next_coordinate = coordinate - [(split_num - 1) * interval, 5]
    for i in tree[now_A]:
        plt.plot([coordinate[0], next_coordinate[0]], [coordinate[1], next_coordinate[1]])
        plt.text((coordinate[0] + next_coordinate[0]) / 2 - 1, (coordinate[1] + next_coordinate[1]) / 2 - 1, s=i,
                 size=12)
        if tree[now_A][i] in labels:
            plt.text(next_coordinate[0], next_coordinate[1], tree[now_A][i], size=15,
                     ha="center", va="center",
                     bbox=dict(boxstyle="circle",
                               ec='blue',
                               fc='blue',
                               )
                     )
        else:
            drawtree(tree[now_A][i], next_coordinate, interval - 4)
        next_coordinate += [interval * 2, 0]


dir = [['青绿', '蜷缩', '浊响', '清晰', '凹陷', '硬滑', 0.697, 0.460, '是'],
       ['乌黑', '蜷缩', '沉闷', '清晰', '凹陷', '硬滑', 0.774, 0.376, '是'],
       ['乌黑', '蜷缩', '浊响', '清晰', '凹陷', '硬滑', 0.634, 0.264, '是'],
       ['青绿', '蜷缩', '沉闷', '清晰', '凹陷', '硬滑', 0.608, 0.318, '是'],
       ['浅白', '蜷缩', '浊响', '清晰', '凹陷', '硬滑', 0.556, 0.215, '是'],
       ['青绿', '稍蜷', '浊响', '清晰', '稍凹', '软粘', 0.403, 0.237, '是'],
       ['乌黑', '稍蜷', '浊响', '稍糊', '稍凹', '软粘', 0.481, 0.149, '是'],
       ['乌黑', '稍蜷', '浊响', '清晰', '稍凹', '硬滑', 0.437, 0.211, '是'],
       ['乌黑', '稍蜷', '沉闷', '稍糊', '稍凹', '硬滑', 0.666, 0.091, '否'],
       ['青绿', '硬挺', '清脆', '清晰', '平坦', '软粘', 0.243, 0.267, '否'],
       ['浅白', '硬挺', '清脆', '模糊', '平坦', '硬滑', 0.245, 0.057, '否'],
       ['浅白', '蜷缩', '浊响', '模糊', '平坦', '软粘', 0.343, 0.099, '否'],
       ['青绿', '稍蜷', '浊响', '稍糊', '凹陷', '硬滑', 0.639, 0.161, '否'],
       ['浅白', '稍蜷', '沉闷', '稍糊', '凹陷', '硬滑', 0.657, 0.198, '否'],
       ['乌黑', '稍蜷', '浊响', '清晰', '稍凹', '软粘', 0.360, 0.370, '否'],
       ['浅白', '蜷缩', '浊响', '模糊', '平坦', '硬滑', 0.593, 0.042, '否'],
       ['青绿', '蜷缩', '沉闷', '稍糊', '稍凹', '硬滑', 0.719, 0.103, '否']]
column = ['色泽', '根蒂', '敲声', '纹理', '脐部', '触感', '密度', '含糖', '好瓜']
data = pd.DataFrame(dir, columns=column)

D = data.drop(columns=['密度', '含糖'], inplace=False)
tree = tree_generate(D, D.columns[:-1])
initial_coordinate = np.array([50, 50])
drawtree(tree, initial_coordinate, 10)
plt.show()
