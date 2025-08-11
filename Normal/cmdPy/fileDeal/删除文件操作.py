# coding=utf-8
# @Time    : 2025/7/28 14:33
# @Software: PyCharm
import os
import platform
import shutil


def remove_java_dir(start_path: str, dir_name: str) -> None:
    """删除某一文件夹下的文件夹

    :param start_path: 父文件夹
    :param dir_name: 待删除的子文件夹
    """
    dir_sum = 0
    for dir_path, dir_names, filenames in os.walk(start_path):
        if dir_name in dir_names:
            shutil.rmtree(os.path.join(dir_path, dir_name))
            dir_sum += 1
    print(f"目录{start_path}下的{dir_sum}个{dir_name}文件夹已清除")


def delete_specific_files(directory: str, file_name_list: list[str]):
    """从一个文件夹中，删除特定的文件

    :param directory: 文件夹的绝对路径
    :param file_name_list: 待删除的文件名称(多个)
    """
    for folder_name, _, filenames in os.walk(directory):  # 使用os.walk进行遍历
        for filename in filenames:
            if filename in file_name_list:  # 如果在遍历过程中找到了指定的文件名
                file_path = os.path.join(folder_name, filename)  # 通过os.path.join连接目录和文件名，得到完整的文件路径
                os.remove(file_path)  # 使用os.remove删除文件
                print(f"Deleted file : {file_path}")  # 输出删除文件的信息


def remove_dir(path):
    if platform.system() == "Windows":
        # Windows系统使用rmdir命令
        run_param = f'rmdir /s /q "{path}"'
    else:
        # Linux/macOS使用rm命令
        run_param = f'rm -rf "{path}"'
    print(f"    --> {run_param}")
    os.system(run_param)


def check_folder_exists(folder_path: str, warn_tit: str):
    """检查路径是否存在且是一个目录

    :param folder_path: 文件夹的绝对路径
    :param warn_tit: 目录存在时的警告文本
    """
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        print(f"--> 文件夹 '{folder_path}' 存在")
        print(warn_tit)
        # 存在则需要手动确认
        is_ok = input("--> 输入Y确认: ")
        return is_ok.upper() == 'Y'
    print(f"--> 文件夹 '{folder_path}' 不存在！")
    return False


if __name__ == '__main__':
    print("""========删除文件夹脚本===========
    1. 删指定目录下java编译文件夹
    2. 删指定目录下特定文件
    0. 删指定目录(默认)""")
    checkFun = input("输入你的选择: ")
    if checkFun == '1':
        # 样例: `E:\MyCode\MixPet`
        java_dir_path = input(r"输入含有Java项目的目录: ")
        warn_txt = f"将会删除 {java_dir_path} 下所有的.idea target .mvn目录"
        if check_folder_exists(java_dir_path, warn_txt):
            remove_java_dir(java_dir_path, '.idea')
            remove_java_dir(java_dir_path, 'target')
            remove_java_dir(java_dir_path, '.mvn')
    elif checkFun == '2':
        parent_dir_path = input(r"输入特定目录: ")
        # 待删除文件，样例：`有标题但不匹配.md, TABLE_ONE.sql`
        need_del_file_str = input("输入多个文件名(逗号分割): ")
        need_del_file = [item.strip() for item in need_del_file_str.split(',')]
        warn_txt = f"将会删除 {parent_dir_path} 下所有的 {need_del_file}"
        if check_folder_exists(parent_dir_path, warn_txt):
            delete_specific_files(parent_dir_path, need_del_file)
    else:
        del_dir_path = input(r"输入需要删的文件夹路径: ")
        warn_txt = f"将会删除整个 {del_dir_path}"
        if check_folder_exists(del_dir_path, warn_txt):
            remove_dir(del_dir_path)
