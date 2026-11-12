# coding=utf-8
# @Time    : 2026/11/12 14:59
# @Software: PyCharm

"""
长文本分割工具（用于SQL插入时，文本过长的解决方案）
"""


def split_text(text: str, size: int) -> list:
    """按字符数切分, 返回分片列表"""
    if size <= 0:
        raise SystemExit("CHUNK_SIZE 必须大于 0")
    return [text[i:i + size] for i in range(0, len(text), size)]


if __name__ == "__main__":
    # 待分割的文本文件
    with open(r"待分割的长文本.txt", encoding="utf-8") as f:
        txt = f.read().strip()
        # 每片字符数; sql脚本建议调成3000
        parts = split_text(txt, 5)

        # 输出可以直接贴进 SQL 的拼接表达式
        for i, part in enumerate(parts, 1):
            # noinspection SqlResolve,SqlNoDataSourceInspection,SqlDialectInspection
            print(f"UPDATE PROC_RE_DEF SET FLOW_CONFIG = FLOW_CONFIG || TO_CLOB('{part}') WHERE BUSI_FLOW_NO = 123;")
