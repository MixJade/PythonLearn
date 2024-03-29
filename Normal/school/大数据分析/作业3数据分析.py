# coding=utf-8
# @Time    : 2022/12/6 22:00
# @Software: PyCharm

import pandas as pd

'''2024年2月4日更新：
这里为了压缩项目大小(去除大的csv文件、减少Jupyter代码)
将原来的”P2P网络贷款数据表“换成了自己生成的csv表
如需要原来的”P2P网络贷款数据表“，请自行去教材对应的官网下载
'''

# class AttemptDataThree(unittest.TestCase):
#     def test_something(self):
#         self.assertEqual(True, False)  # add assertion here
#
#
# if __name__ == '__main__':
#     unittest.main()

"""实训1读取并查看P2P网络贷款数据主表的基本信息
书P130
使用ndim、 shape、 memory_usage属性分别查看维度、大小、占用内存信息
使用describe方法进行描述性统计,并剔除值相同或全为空的列。
"""
# (1)通过Pandas读取csv
train_csv = pd.read_csv('../A1输入数据/train_data.csv', sep=',', encoding='utf-8')
print(train_csv)

# (2)使用ndim、shape、memory_usage属性分别查看维度、大小、占用内存信息
print("1. 主表的维度为", train_csv.ndim)
print("2. 主表的大小为", train_csv.shape)
print("3. 主表的每一列以及索引占用内存为（只显示前五行）\n", train_csv.memory_usage().head())  # 只查看前五行
print("\n============以下题外话==============")
print("4. 主表的索引为", train_csv.index)
print("5. 主表的元素个数为", train_csv.size)
print("6. 主表的列名为（只显示前八个）:\n", train_csv.columns[0:8])
print("\n7. 主表的元素类型为（dataframe内数据类型可以不一样）\n", train_csv.dtypes)

# (3)使用describe方法进行描述性统计,并剔除值相同或全为空的列。
# 3.1 使用describe方法进行描述性统计
master_describe = train_csv.describe()
print(master_describe)


# 3.2 剔除值相同或全为空的列(书P106)
def del_same_null(table_name, data):
    """
    剔除值相同或全为空的列
    """
    before_del = data.shape[1]
    null_column = data.describe().loc["count"] == 0
    for i in range(len(null_column)):
        if null_column.iloc[i]:
            data.drop(labels=null_column.index[i], axis=1, inplace=True)
    same_column = data.describe().loc["std"] == 0
    for j in range(len(same_column)):
        if same_column.iloc[j]:
            data.drop(labels=same_column.index[j], axis=1, inplace=True)
    after_del = data.shape[1]
    del_sum = before_del - after_del
    print("{}表，剔除了{}列，剔除后形状为：{}".format(table_name, del_sum, data.shape))


# 执行剔除方法
del_same_null("主", train_csv)

"""实训2：提取用户信息更新表和登录相关信息表的时间信息
书P130
使用to_datetime函数转换用户信息更新表和登录信息表的时间字符串。
使用year、 month、week等方法提取用户信息更新表和登录信息表中的时间信息
计算用户信息更新表和登录信息表中两时间的差,分别以日、小时、分钟计算。
"""
# (1)使用to_datetime函数转换用户信息更新表和登录信息表的时间字符串。
train_csv["登录日期"] = pd.to_datetime(train_csv["登录日期"])
train_csv["注册日期"] = pd.to_datetime(train_csv["注册日期"])
train_csv["导出日期"] = pd.to_datetime(train_csv["导出日期"])
# 查看时间字符串的类型
print("时间字符串的类型为", train_csv["登录日期"].dtype)


# (2)使用year、 month、week等方法提取用户信息更新表和登录信息表中的时间信息
def show_time(info, data):
    year = [i.year for i in data.head()]
    print("{}，前5个年份信息：{}".format(info, year))
    month = [i.month for i in data.head()]
    print("{}，前5个月份信息：{}".format(info, month))
    week = [i.week for i in data.head()]
    print("{}，前5个星期信息：{}".format(info, week))
    day = [i.day for i in data.head()]
    print("{}，前5个日期信息：{}".format(info, day), end='\n\n')


# 查看时间信息
show_time("训练数据，登录日期", train_csv["登录日期"])
show_time("训练数据，注册日期", train_csv["注册日期"])

# (3)计算用户信息更新表和登录信息表中两时间的差
# > 分别以日、小时、分钟计算。
# 试射：计算用户信息更新表和登录信息表中两时间的差
date_bad = train_csv["导出日期"] - train_csv["登录日期"]
print("计算时间差以日期为单位：\n", date_bad.head())
print("时间字符串的类型为", date_bad.dtype)


def hour_bad(data):
    hour_list = []
    for i in range(len(data)):
        hour_list.append(data[i].total_seconds() / 3600)
    return hour_list


print("计算时间差以小时为单位：\n", hour_bad(date_bad)[:5])


def minute_bad(data):
    minute_list = []
    for i in range(len(data)):
        minute_list.append(data[i].total_seconds() / 60)
    return minute_list


print("计算时间差以分钟为单位：\n", minute_bad(date_bad)[:5])

"""实训3:使用分组聚合方法进一步分析用户信息更新表和登录信息表
使用group_by方法对用户信息更新表和登录信息表进行分组
使用agg方法求取分组后的最早和最晚更新及登录时间。
使用size方法求取分组后的数据的信息更新次数与登录次数。
"""
print("登录日期参数类型", train_csv.dtypes["登录日期"])
# (1)使用group_by进行分组
login_nm_group = train_csv[["姓名", "登录日期"]].groupby(by="姓名")
print(login_nm_group.head())

# (2)使用agg方法求取分组后的最早和最晚登录日期。
# 这个分组是前面的group_by
print("分组后最早登录日期:\n", login_nm_group.agg("min").head())
print("分组后最晚登录日期:\n", login_nm_group.agg("max").head())
print()

# (3)使用size方法求取分组后数据的登录日期出现次数。
print("登录日期出现次数：\n", login_nm_group.size().head())
