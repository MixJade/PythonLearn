# coding=utf-8
# @Time    : 2025/4/18 13:59
# @Software: PyCharm
from pathlib import Path


def get_folder_size(folder_path: str) -> int:
    """获取文件夹的大小(不重复计算硬链接)

    :param folder_path: 文件夹路径
    :return: 文件夹的字节长度
    """
    total_size = 0
    st_ino_num: int = 0  # 硬链接数量
    # 用于存储已计算过的inode
    inodes = set()
    folder = Path(folder_path)
    for item in folder.rglob('*'):
        if item.is_file():
            try:
                stat = item.stat()
                # 检查inode是否已经计算过
                if stat.st_ino not in inodes:
                    total_size += stat.st_size
                    inodes.add(stat.st_ino)
                else:
                    st_ino_num += 1
            except OSError:
                print(f"无法访问文件 {item}")
    print(f"文件夹 {folder_path} 中存在 {st_ino_num} 个硬链接")
    return total_size


def convert_file_size(length: int) -> str:
    """转换文件大小

    :param length: 文件字节长度
    :return: 文件通用的大小单位(KB/MB)
    """
    if length < (1 << 10):
        # 小于1kb则以b为单位
        file_size = f"{length}B"
    elif length < (1 << 20):
        # 小于1mb则kb单位
        int_part = length >> 10  # 整数部分
        dec_part = ((length - (int_part << 10)) * 100) >> 10  # 小数部分(x100保留两位小数)
        file_size = f"{int_part}.{dec_part}KB"
    else:
        # 其余mb单位
        int_part = length >> 20  # 整数部分
        dec_part = ((length - (int_part << 20)) * 100) >> 20  # 小数部分(x100保留两位小数)
        file_size = f"{int_part}.{dec_part}MB"
    return file_size


# 示例用法
ts_folder_path = r'../../../TsLearn'
size = get_folder_size(ts_folder_path)
print(f"文件夹 {ts_folder_path} 的大小是 {size} 字节({convert_file_size(size)})")
