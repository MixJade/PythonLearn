# coding=utf-8
# @Time    : 2025/9/17 16:14
# @Software: PyCharm
import pandas as pd

data1 = pd.read_csv(r'待读取数据.csv')[['NAME', 'COMMENT', 'CATE']]

for index1, row1 in data1.iterrows():
    # 使用at函数修改
    data1.at[index1, 'CATE'] = f'修改后的内容{index1}'
    print(f"name: {row1['NAME']} comment: {row1['COMMENT']}  cate: {row1['CATE']} ")

# 导出为csv(可指定字段范围)
out_file_name = '待读取数据_结果.csv'
data1[['NAME', 'COMMENT', 'CATE']].to_csv(
    out_file_name,
    index=False,
    encoding='utf-8-sig'
)
print(f"\nCSV 文件:【{out_file_name}】已生成！")
