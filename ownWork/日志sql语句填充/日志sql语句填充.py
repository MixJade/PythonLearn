# coding=utf-8
# @Time    : 2025/9/15 10:56
# @Software: PyCharm
def replace_question_marks(sql_str, values_str):
    """将SQL语句中的问号替换为带中括号的字符串中的对应元素

    :param sql_str: 包含问号占位符的SQL字符串
    :param values_str: 带中括号的字符串，格式如"[值1, 值2, 值3]"
    :return: 替换后的SQL字符串
    """
    # 处理值字符串：去除中括号并分割元素
    # 去除首尾的中括号
    cleaned_str = values_str.strip('[]')
    # 分割元素并去除每个元素的前后空格
    values = [item.strip() for item in cleaned_str.split(',')]

    # 检查问号数量和值的数量是否匹配
    question_count = sql_str.count('?')
    if question_count != len(values):
        return f"问号数量({question_count})与值的数量({len(values)})不匹配"

    # 替换问号
    result = sql_str
    for value in values:
        # 替换第一个问号(值一律加单引号)
        result = result.replace('?', f"'{value}'", 1)
    return result


# 示例用法
if __name__ == "__main__":
    # SQL语句
    # noinspection SqlNoDataSourceInspection,SqlDialectInspection,SqlResolve
    sql = "UPDATE Dog set dogName=?, dogSex = ?,dogAge= ? WHERE dogId = ?"

    # 带中括号的字符串
    sql_param_str = "[旺财, 母, 23, 38]"

    replaced_sql = replace_question_marks(sql, sql_param_str)
    print("替换后的SQL语句:")
    print(replaced_sql)
