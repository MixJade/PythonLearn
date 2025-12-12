# coding=utf-8
# @Time    : 2025/12/12 16:12
# @Software: PyCharm
import os
import re


def batch_replace_form_id(folder_path):
    """
    批量替换文件夹下所有文件中的 :form-id="'数字'" 为 formId="数字"
    """
    # 定义正则表达式：匹配 form-id="'数字串'" 格式
    # 捕获组1：数字串，支持任意长度的数字
    # 如果需要同时匹配单引号和双引号，使用这个pattern：
    pattern = re.compile(r':form-id="\'(\d+)\'"')

    # 遍历文件夹下所有文件
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            # 拼接文件完整路径
            file_path = os.path.join(root, file_name)
            # 跳过非vue文件
            if not file_name.endswith('.vue'):
                continue

            try:
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                matches = pattern.findall(content)
                if matches:
                    print(f"\n【{file_path}】匹配到的内容：")
                    # 输出完整匹配文本（带form-id前缀）
                    full_matches = pattern.findall(content)  # 获取捕获组内容
                    # 还原完整匹配字符串
                    full_match_texts = [f'form-id="{match}"' for match in full_matches]
                    for idx, match_text in enumerate(full_match_texts, 1):
                        print(f"  匹配项{idx}: {match_text}")
                    # 输出仅数字部分
                    print(f"  提取的数字列表: {matches}")
                # 替换内容
                new_content = pattern.sub(r'formId="\1"', content)

                # 如果内容没有变化，跳过
                if new_content == content:
                    continue

                # 写入替换后的内容
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

                print(f"成功处理文件: {file_path}")

            except Exception as e:
                print(f"处理文件 {file_path} 失败: {str(e)}")


if __name__ == "__main__":
    # 请修改为你的目标文件夹路径
    target_folder = r"D:\proj\frontend\prod-ui\src"

    # 检查文件夹是否存在
    if not os.path.isdir(target_folder):
        print(f"错误：文件夹 {target_folder} 不存在！")
    else:
        print(f"开始处理文件夹: {target_folder}")
        print("=" * 50)
        batch_replace_form_id(target_folder)
        print("=" * 50)
        print("处理完成！")
