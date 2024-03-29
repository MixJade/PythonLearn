# coding=utf-8
# @Time    : 2024/3/1 17:07
# @Software: PyCharm
import os


def replace_content_in_two_lines(file_path: str, content: str) -> None:
    """
    详情见替换指定两行间的内容中的replace_content_in_two_lines方法
    """
    with open(file_path, encoding="utf-8") as f:
        lines = f.readlines()
    start_index = next(index for index, line in enumerate(lines) if "// 天地自然，秽炁分散。" in line)
    end_index = next(index for index, line in enumerate(lines) if "// 乾罗答那，洞罡太玄；" in line)
    lines[start_index + 1:end_index] = [content]
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"文件:‘{file_path}’的内容替换成功")


def list_files(dir_path: str) -> dict[str, str | list]:
    """读取文件下的目录结构，并输出成vuePress的配置文件形式

    :param dir_path: 目标文件夹
    """
    result = {'text': os.path.basename(dir_path), 'collapsible': 'true', 'children': []}

    # 遍历目录下的所有子目录和文件
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)

        # 如果是文件，则直接添加文件名
        if os.path.isfile(item_path):
            children_str: str = item_path.replace(target_dir, "").replace("\\", "/")
            result['children'].append(children_str)
        # 如果是目录，则递归调用该函数
        else:
            result['children'].append(list_files(item_path))

    return result


# 目标文件夹
# 存放代码的公共文件夹
# (当前文件的上三级目录)等价于r"C:\MyCode"
code_dir = os.path.abspath(os.path.join(os.getcwd(), "../../../.."))
target_dir = code_dir + r"\TsLearn\my-page\docs"

# 输出的字符串
result_str: str = 'sidebar: {\n'

# javaLearn的文件夹输出结构
files_list = list_files(target_dir + r"\javaLearn")
result_str += r'"/javaLearn/": '
result_str += files_list['children'].__str__()
result_str += ',\n'
# tsLearn的文件夹输出结构
files_list = list_files(target_dir + r"\tsLearn")
result_str += r'"/tsLearn/": '
result_str += files_list['children'].__str__()
result_str += ',\n'
# pyLearn的文件夹输出结构
files_list = list_files(target_dir + r"\pyLearn")
result_str += r'"/pyLearn/": '
result_str += files_list['children'].__str__()
result_str += ',\n'

# 最终输出
result_str += '},\n'
print(result_str)

# 然后写入
replace_content_in_two_lines(target_dir + r"\.vuepress\config.js",
                             content=result_str)
