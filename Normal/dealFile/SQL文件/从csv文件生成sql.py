# coding=utf-8
# @Time    : 2024/3/7 17:43
# @Software: PyCharm
import warnings


# 消除pandas低版本的默认警告
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    import pandas as pd

# 输入的csv文件
inputFile = '../../inputFile/SQL文件/待删除数据.csv'

try:
    # 读取CSV文件(如果读取失败，请手动将对应csv文件转为utf8格式)
    df = pd.read_csv(inputFile, encoding='utf-8')
except UnicodeDecodeError:
    # 使用utf-8读取失败,尝试原始编码读取
    df = pd.read_csv(inputFile, encoding='mbcs')

# 获取需要的列
df = df[['HOME_ID', 'DOG_TP', 'DOG_ID', '是否保留']]

# 逐行打印SQL语句，同时需要保留的数据不删
for index, row in df.iterrows():
    if row['是否保留'] != '保留':
        print(f"DELETE HomeAndDog "
              f"WHERE homeID='{row['HOME_ID']}' "
              f"AND dogID ='{row['DOG_ID']}' "
              f"AND dogTP='{row['DOG_TP']}';")
