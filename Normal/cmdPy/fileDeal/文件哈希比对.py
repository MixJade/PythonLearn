# coding=utf-8
# @Time    : 2026/1/4 11:06
# @Software: PyCharm
import hashlib
import os


def calculate_file_hash(file_path):
    """计算文件的哈希值（分块读取避免内存溢出）

    :param file_path: 目标文件的路径
    :return: 文件的十六进制哈希字符串；若文件不存在/无法访问，返回None
    """
    # 校验文件是否存在且可访问
    if not os.path.isfile(file_path):
        print(f"错误：文件 '{file_path}' 不存在或不是一个有效文件")
        return None

    # 初始化哈希对象
    hash_obj = hashlib.new("md5")
    # 快速获取文件总字节长度
    total_bytes = os.path.getsize(file_path)
    print(f"文件总字节长度：{total_bytes} 字节")
    # 分块读取文件并更新哈希值（支持大文件）
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(4096):  # 逐块读取文件内容
                hash_obj.update(chunk)
        return hash_obj.hexdigest()  # 返回十六进制哈希字符串
    except PermissionError:
        print(f"错误：没有权限读取文件 '{file_path}'")
        return None
    except Exception as e:
        print(f"错误：读取文件 '{file_path}' 失败，异常信息：{str(e)}")
        return None


if __name__ == "__main__":
    # 初始化存储文件路径与哈希值的map（字典）
    file_hash_map = {}
    print("===== 文件哈希对比工具 =====")
    while True:
        file_path_str = input("\n输入文件路径(0退出)：").strip()
        if file_path_str == '0' or file_path_str == '':
            break
        else:
            first_file_hash = calculate_file_hash(file_path_str)
            if first_file_hash:
                print(f"  文件哈希：{first_file_hash}")
                if first_file_hash in file_hash_map:
                    print(f"\n【提示】该文件的哈希值已存在！")
                    print(f"  匹配的文件路径：{file_hash_map[first_file_hash]}")
                # 存储：键为哈希值，值为文件路径
                file_hash_map[first_file_hash] = file_path_str
            else:
                print("文件处理失败，程序无法继续执行")
                break
