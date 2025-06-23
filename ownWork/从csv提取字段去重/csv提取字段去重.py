# coding=utf-8
# @Time    : 2025/6/20 15:28
# @Software: PyCharm
import pandas as pd

df = pd.read_csv('有重复描述的字段.csv')
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


def camel_to_snake(name):
    """
    将小驼峰格式字符串转为大蛇形格式
    示例：prjName → PRJ_NAME
    """
    # 用于存储转换后的字符列表
    snake_case = []
    for i, char in enumerate(name):
        # 若当前字符是大写字母，并且不是字符串的第一个字符
        if char.isupper() and i > 0:
            # 前一个字符是小写字母时添加下划线
            if name[i - 1].islower():
                snake_case.append('_')
        # 把当前字符添加到结果列表
        snake_case.append(char)
    # 把列表组合成字符串并转为大写
    return ''.join(snake_case).upper()


# 打印添加字段的sql
print("\n" + ("=" * 100) + "\n")
for index, row in df_agg3_sorted.iterrows():
    # noinspection SqlResolve,SqlNoDataSourceInspection,SqlDialectInspection
    print(f"""-- {row["comment"]}({row["cate"]})({row["dict"]})
ALTER TABLE MY_TABLE
ADD {camel_to_snake(row["field"])} VARCHAR2(200) NULL;
COMMENT ON COLUMN MY_TABLE.{camel_to_snake(row["field"])} IS '{row["comment"]}';""")

# 打印字段核对sql
print("\n" + ("=" * 100) + "\n")
# 将NAME列的值用双引号包裹并聚合
name_result = ','.join([f"'{camel_to_snake(name)}'" for name in df_agg3_sorted['field']])
# noinspection SqlResolve,SqlNoDataSourceInspection,SqlDialectInspection
print(f"""
-- 检查表字段 预计{len(df_agg3_sorted)}条
SELECT COLUMN_NAME
FROM USER_TAB_COLUMNS
WHERE TABLE_NAME = 'MY_TABLE'
  AND COLUMN_NAME IN ({name_result});
""")
