# coding=utf-8
# @Time    : 2022/11/29 21:52
# @Software: PyCharm
import pandas as pd

print("\n=====一、导入数据=====")
plague01 = pd.read_excel('../A1输入数据/plague-data.xlsx')  # 导入疫情数据
print(plague01.head())  # 只看前五个

# 二、处理日期格式数据(书P109)
print("\n=====二、处理日期格式数据(书P109)=====")
print("转化前日期类型:", plague01['日期'].dtypes)
plague01['日期'] = pd.to_datetime(plague01['日期'])
print("转化后日期类型:", plague01['日期'].dtypes)

# 三、提取日期常用数据
print("\n=====三、提取日期常用数据=====")
# 1. 年
year = [i.year for i in plague01['日期']]
print("第十条数据的年份:", year[10])
# 2. 月
print("第十条数据的月份:", plague01['日期'][10].month)
# 3. 日
print("第十条数据的月份:", plague01['日期'][10].day)
# 4. 星期几
print("第十条数据的星期:", plague01['日期'][10].weekday())
# 5. 星期几的英文
print("第十条数据的星期:", plague01['日期'][10].day_name())

# 四、对数据进行分组聚合(书P114)
print("\n=====四、对数据进行分组聚合(书P114)=====")
# 1. group-by
group = plague01[['省份', '死亡']].groupby(by='省份')
print("分组后的数据(group-by)\n", group.head())

# 2. agg
print("死亡增量与治愈增量的和与均值(agg)", )
print(plague01[['死亡增量', '治愈增量']].agg(("sum", "mean")))
# 3. apply方法见书P119

# 五、创建透视表与交叉表(书P123)
print("\n=====五、创建透视表与交叉表(书P123)=====")
# 5.1. 透视表
print("5.1 透视表")
plague01_pivot01 = pd.pivot_table(plague01[['省份', '死亡', '治愈']], index='省份', aggfunc="sum")  # 指定是数据和,默认是数据的均值
print(plague01_pivot01.head())

# 5.2. 透视表
print("5.2 透视表")
plague01_pivot02 = pd.pivot_table(plague01[['日期', '省份', '死亡', '治愈']], index='日期', columns='省份',
                                  values='死亡', aggfunc="sum")
print(plague01_pivot02.head())

# 课堂练习
# 创建透视表，展示每日累计确诊和现有确诊增量
# 创建交叉表, 展示每日每省累计确诊
print("\n=====六、课堂练习，创建透视表、交叉表=====")
# 透视表
print("课堂练习(透视表)")
plague01_pivot03 = pd.pivot_table(plague01[[
    '日期', '累计确诊', '现有确诊增量']],
                                  index='日期', aggfunc="sum")  # 指定是数据和,默认是数据的均值
print(plague01_pivot03.head())

# 交叉表
print("课堂练习(交叉表)")
plague01_cross_tab = pd.crosstab(index=plague01['省份'],
                                 columns=plague01['日期'],
                                 values=plague01['累计确诊'], aggfunc="sum")
print(plague01_cross_tab.head())
