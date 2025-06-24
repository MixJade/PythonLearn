# coding=utf-8
# @Time    : 2025/6/20 15:28
# @Software: PyCharm
import pandas as pd

df = pd.read_csv('input/有重复描述的字段.csv')
df = df[['cate', 'dict', 'field', 'comment']]

# 开始去重(指定列)，保留第一次出现的重复行
df_unique2 = df.drop_duplicates(subset=['cate', 'dict', 'field'])

# 基于field列去重，同时聚合多列
df_agg3 = df_unique2.groupby('field').agg({
    'cate': lambda x: '、'.join(sorted(set(x))),  # 聚合时也顺便去重
    'dict': lambda x: '、'.join(sorted(set(x))),
    'comment': lambda x: '、'.join(sorted(set(x)))
}).reset_index()

# 按分类排序
df_agg3_sorted = df_agg3.sort_values('field').sort_values('dict')
# 确定以上的没问题之后，输出
for index, row in df_agg3_sorted.iterrows():
    print(f"""
    /**
     * {row["comment"]}
     * - {row["cate"]}
     * - {row["dict"]}
     */
    private String {row["field"]};""")


def camel_to_snake(name: str) -> str:
    """
    将小驼峰格式字符串转为大蛇形格式
    示例：prjName → PRJ_NAME
    """
    # 用于存储转换后的字符列表
    snake_case = []
    for i, char in enumerate(name):
        # 若当前字符是大写字母，并且不是字符串的第一个字符
        if char.isupper() and i > 0:
            # 前一个字符是小写字母或数字时添加下划线
            if name[i - 1].islower() or name[i - 1].isdigit():
                snake_case.append('_')
        # 把当前字符添加到结果列表
        snake_case.append(char)
    # 把列表组合成字符串并转为大写
    return ''.join(snake_case).upper()


# 生成添加字段的csv
print("\n" + ("=" * 100) + "\n")
# 添加一个新列
df_agg3_sorted['COLUMN_NAME'] = df_agg3_sorted['field'].apply(camel_to_snake)

# 临时重命名并导出
df_agg3_sorted[['COLUMN_NAME', 'comment', 'cate', 'dict']].to_csv(
    '生成的字段.csv',
    index=False,
    encoding='utf-8-sig'
)

print("CSV 文件已生成！")
