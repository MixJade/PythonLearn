# coding=utf-8
# @Time    : 2024/3/27 14:59
# @Software: PyCharm
import pandas as pd

# 读取CSV文件(如果读取失败，请将对应csv文件转为utf8格式)
inputCsv: str = '待解压数据.csv'
df = pd.read_csv(inputCsv)

# 获取需要的列
df = df[['Number', 'Name', 'UserRole', 'UserID']]

# 首先把'USR_NO'列中的字符串通过','分割然后转换为列表
df['UserID'] = df['UserID'].str.split(',')

# 然后利用explode来拆分一行为多行(爆炸函数)
df = df.explode('UserID')

df = df.sort_values('Number')
# 重设索引
df = df.reset_index(drop=True)

# 打印输出(调试所用)
print(df.head(n=9))

# 保存为新的csv文件
df.to_csv(inputCsv.replace('.csv', '结果.csv'), index=False)
